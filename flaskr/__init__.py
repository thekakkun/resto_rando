import os

from flask import Flask, jsonify

from flaskr import api
from flaskr.auth import AuthError
from flaskr.models import db, migrate

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DATABASE_URL = os.environ.get('DATABASE_URL', None)
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        DB_NAME = 'resto_rando'

        if not DATABASE_URL:
            app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        DB_NAME = 'resto_rando_test'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api.bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'The server can not find the requested resource.'
        }), 404

    @app.errorhandler(405)
    def not_allowed(e):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'The method is not allowed.'
        }), 405

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'The request was well-formed but was unable to be followed due to semantic errors.'
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            'success': False,
            'error': e.status_code,
            'message': e.error['description']
        }, e.status_code)

    return app


def setup_database(app):
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app = create_app()
    setup_database(app)
    app.run()
