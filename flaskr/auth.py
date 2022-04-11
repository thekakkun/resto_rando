from functools import wraps

import jwt
from flask import request

AUTH0_DOMAIN = 'dev-2m33ryh3.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'resto'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'authorization header is missing',
            'description': 'Authorization header is expected.'
        }, 401)

    try:
        schema, token, *other = auth.split()
    except ValueError:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Token not found.'
        }, 401)

    if schema.lower() != 'bearer':
        raise AuthError({
            'code': 'invalid header',
            'description': 'The authorization schema used must be "Bearer."'
        }, 401)
    elif other:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    return token


def check_permission(permission, payload):
    allowed = payload.get('permissions', None)

    if not allowed:
        raise AuthError({
            'code': 'forbidden',
            'description': 'No permissions in payload.'
        }, 403)
    elif permission not in allowed:
        raise AuthError({
            'code': 'forbidden',
            'description': 'Action not allowed for user/role.'
        }, 403)
    else:
        return True


def verify_decode_jwt(token):
    header = jwt.get_unverified_header(token)
    if 'kid' not in header:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Authorization malformed.'
        }, 401)

    url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    jwks_client = jwt.PyJWKClient(url)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=ALGORITHMS,
            options={'require': ['exp', 'iss', 'aud']},
            audience=API_AUDIENCE,
            issuer=f'https://{AUTH0_DOMAIN}/'
        )
        return data

    except jwt.MissingRequiredClaimError:
        raise AuthError({
            'code': 'invalid claims',
            'description': 'Missing required claims.'
        }, 401)
    except jwt.InvalidKeyError:
        raise AuthError({
            'code': 'invalid key',
            'description': 'Key is not in the required format.'
        }, 401)
    except jwt.InvalidIssuerError:
        raise AuthError({
            'code': 'invalid issuer',
            'description': '"iss" claim does not match expected issuer.'
        }, 401)
    except jwt.InvalidAudienceError:
        raise AuthError({
            'code': 'invalid audience',
            'description': '"aud" claim odes not match expected audience.'
        }, 401)
    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token expired',
            'description': 'Signature does not match the one provided.'
        }, 401)
    except jwt.DecodeError:
        raise AuthError({
            'code': 'decode error',
            'description': 'Token failed validation.'
        }, 400)
    except jwt.InvalidTokenError:
        raise AuthError({
            'code': 'invalid token',
            'description': 'Token could not be decoded.'
        }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permission(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
