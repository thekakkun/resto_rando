from datetime import datetime
from random import choice

from flask import Blueprint, abort, jsonify, request

from flaskr.auth import AuthError, check_permission, requires_auth
from flaskr.models import Account, Category, Restaurant, db

ITEMS_PER_PAGE = 10

bp = Blueprint('api', __name__, url_prefix='/api')


def paginate(restaurants, page):
    '''
    Slice list of restaurants to page specified.
    Size of page is specified by ITEMS_PER_PAGE.
    '''
    page_start = (page - 1) * ITEMS_PER_PAGE
    page_end = page_start + ITEMS_PER_PAGE
    return restaurants[page_start:page_end]


def parse_date(date_str=None):
    '''
    Return datetime object based on string submitted by user.
    '''
    if not date_str:
        return None
    elif date_str.lower() == 'today':
        return datetime.today()
    else:
        return datetime.fromisoformat(date_str)


@bp.route("/categories", methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
    except:
        abort(422)

    return jsonify({
        'success': True,
        "categories": {cat.id: cat.name for cat in categories}
    }), 200


@bp.route("/restaurants", methods=['GET'])
@requires_auth('get:my_resto')
def get_resto(payload):
    try:
        subject = payload['sub']
        account = Account.query.filter_by(name=subject).one_or_none()
        user = request.args.get('user', default=0, type=int)

        if user:
            if user == account.id:
                restaurants = Restaurant.query.filter_by(account_id=account.id)
            elif check_permission('get:any_resto', payload):
                restaurants = Restaurant.query.filter_by(account_id=user)
        else:
            try:
                if check_permission('get:any_resto', payload):
                    restaurants = Restaurant.query
            except AuthError:
                restaurants = Restaurant.query.filter_by(account_id=account.id)

        cat = request.args.get('category', default=None, type=str)
        if cat:
            restaurants = restaurants.filter(
                Restaurant.categories.any(Category.name.in_([cat])))

        search_term = request.args.get('q', default=None, type=str)
        if search_term:
            restaurants = restaurants.filter(
                Restaurant.name.ilike(f"%{search_term}%"))

        page = request.args.get('page', default=1, type=int)

    except AuthError as e:
        raise e
    except:
        abort(422)

    return jsonify({
        'success': True,
        'category': cat,
        'count': restaurants.count(),
        'page': page,
        'restaurants': [resto.out() for resto in paginate(restaurants, page)]
    }), 200


@bp.route("/restaurants", methods=['POST'])
@requires_auth('post:resto')
def post_resto(payload):
    try:
        data = request.json
        subject = payload['sub']

        user = Account.query.filter_by(name=subject).one_or_none()
        if not user:
            db.session.add(Account(name=subject))
            db.session.commit()

        resto = Restaurant(
            name=data['name'],
            address=data['address'],
            visited=data.get('visited', False),
            account_id=Account.query.filter_by(name=subject).first().id
        )
        for cat in data['categories']:
            resto.categories.append(
                Category.query.filter_by(name=cat).first())

        if 'date_visited' in data:
            visit_date = parse_date(data['date_visited'])
            resto.date_visited = visit_date
            resto.visited = True if visit_date else False

        resto.insert()

    except:
        abort(422)

    return get_resto()


@bp.route("/restaurants/<int:resto_id>", methods=['PATCH'])
@requires_auth('patch:my_resto')
def edit_resto(payload, resto_id):
    try:
        resto = Restaurant.query.get(resto_id)
        if not resto:
            abort(404)

        subject = payload['sub']
        account = Account.query.filter_by(name=subject).one_or_none()
        if resto.account.id != account.id:
            check_permission('patch:any_resto', payload)

        data = request.json
        resto.name = data.get('name', resto.name)
        resto.address = data.get('address', resto.address)
        resto.visited = data.get('visited', resto.visited)

        if 'categories' in data:
            resto.categories = []
            for cat in data['categories']:
                resto.categories.append(
                    Category.query.filter_by(name=cat).first())

        if 'date_visited' in data:
            visit_date = parse_date(data['date_visited'])
            resto.date_visited = visit_date
            resto.visited = True if visit_date else False

        resto.update()

    except AuthError as e:
        raise e
    except Exception as e:
        abort(e.code) if e.code else abort(422)

    return get_resto()


@bp.route("/restaurants/<int:resto_id>", methods=['DELETE'])
@requires_auth('delete:my_resto')
def delete_resto(payload, resto_id):
    try:
        resto = Restaurant.query.get(resto_id)
        if not resto:
            abort(404)

        subject = payload['sub']
        account = Account.query.filter_by(name=subject).one_or_none()
        if resto.account.id != account.id:
            check_permission('delete:any_resto', payload)

        resto.delete()

    except AuthError as e:
        raise e
    except Exception as e:
        abort(e.code) if e.code else abort(422)

    return get_resto()


@bp.route("/random", methods=['GET'])
@requires_auth('get:my_resto')
def rando_resto(payload):
    try:
        subject = payload['sub']
        account = Account.query.filter_by(name=subject).one_or_none()

        restaurants = Restaurant.query.filter_by(account_id=account.id)

        cat = request.args.get('category', default=None, type=str)
        if cat:
            restaurants = restaurants.filter(
                Restaurant.categories.any(Category.name.in_([cat])))

        new = 'new' in request.args
        if new:
            restaurants = restaurants.filter(Restaurant.visited == new)

    except:
        abort(422)

    return jsonify({
        'success': True,
        'category': cat,
        'new': new,
        'restaurants': [choice(restaurants.all()).out()] if restaurants else None
    }), 200
