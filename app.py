import json
import os
from datetime import datetime
from random import choice

from flask import Flask, abort, jsonify, request
from flask_migrate import Migrate

from models import Account, Category, Restaurant, db

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/resto_rando'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)

# TODO: pagination
# TODO: unit testing


def parse_date(date_str):
    if not date_str:
        return None
    elif date_str == 'today':
        return datetime.today()
    else:
        return datetime.fromisoformat(date_str)


@app.route("/api/categories", methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
    except:
        abort(422)

    return jsonify({
        'success': True,
        "categories": {cat.id: cat.name for cat in categories}
    }), 200


@app.route("/api/<int:cat_id>/restaurants", methods=['GET'])
def get_resto_by_cat(cat_id):
    try:
        cat = Category.query.get(cat_id)
        if not cat:
            abort(404)

    except Exception as e:
        abort(err.code) if e.code else abort(422)

    return jsonify({
        'success': True,
        'category': cat.name,
        'restaurants': [resto.out() for resto in cat.restaurants]
    }), 200


@app.route("/api/restaurants", methods=['GET'])
def get_resto():
    try:
        restaurants = Restaurant.query.all()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'category': None,
        'restaurants': [resto.out() for resto in restaurants]
    }), 200


@app.route("/api/restaurants", methods=['POST'])
def add_resto():
    try:
        data = request.json

        if 'search_term' in data:
            restaurants = Restaurant.query.filter(
                Restaurant.name.ilike(f"%{data['search_term']}%")).all()
        else:
            resto = Restaurant(
                name=data['name'],
                address=data['address'],
                visited=data.get('visited', False),
                account_id=1  # TODO: update once user accounts are implemented
            )
            for cat in data['categories']:
                resto.categories.append(
                    Category.query.filter_by(name=cat).first())

            if 'date_visited' in data:
                visit_date = parse_date(data['date_visited'])
                resto.date_visited = visit_date
                resto.visited = True if visit_date else False

            db.session.add(resto)
            db.session.commit()

            restaurants = Restaurant.query.all()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'category': None,
        'restaurants': [resto.out() for resto in restaurants]
    }), 200


@app.route("/api/restaurants/<int:resto_id>", methods=['PATCH'])
def edit_resto(resto_id):
    try:
        data = request.json
        resto = Restaurant.query.get(resto_id)

        if not resto:
            abort(404)

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

        db.session.commit()

        restaurants = Restaurant.query.all()

    except Exception as e:
        abort(err.code) if e.code else abort(422)

    return jsonify({
        'success': True,
        'category': None,
        'restaurants': [resto.out() for resto in restaurants]
    }), 200


@app.route("/api/restaurants/<int:resto_id>", methods=['DELETE'])
def delete_resto(resto_id):
    try:
        resto = Restaurant.query.get(resto_id)
        if not resto:
            abort(404)
        db.session.delete(resto)
        db.session.commit()

        restaurants = Restaurant.query.all()

    except Exception as e:
        abort(err.code) if e.code else abort(422)

    return jsonify({
        'success': True,
        'category': None,
        'restaurants': [resto.out() for resto in restaurants]
    }), 200


@app.route("/api/random", methods=['POST'])
def rando_resto():
    try:
        data = request.json

        if data:
            restaurants = db.session.query(Restaurant)
            if 'category' in data:
                restaurants = restaurants.filter(
                    Restaurant.categories.any(Category.name.in_([data['category']])))
            if 'visited' in data:
                restaurants = restaurants.filter(
                    Restaurant.visited == data['visited'])

            restaurants = restaurants.all()

        else:
            restaurants = Restaurant.query.all()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'restaurants': [choice(restaurants).out()] if restaurants else None
    }), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'The server can not find the requested resource.'
    }), 404


@app.errorhandler(422)
def unprocessable(e):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'The request was well-formed but was unable to be followed due to semantic errors.'
    }), 422
