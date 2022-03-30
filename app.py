import os

from flask import Flask, jsonify, request
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


@app.route("/api/categories", methods=['GET'])
def get_categories():
    categories = Category.query.all()

    return jsonify({
        'success': True,
        "categories": {cat.id: cat.name for cat in categories}
    })


@app.route("/api/<int:cat_id>/restaurants", methods=['GET'])
def get_resto_by_cat(cat_id):
    return jsonify({
        'success': True
    })


@app.route("/api/restaurants", methods=['GET'])
def get_resto():
    return jsonify({
        'success': True,
    })


@app.route("/api/restaurants", methods=['POST'])
def add_resto():
    data = request.json

    resto = Restaurant(
        name=data['name'],
        address=data['address'],
        visited=data.get('visited', False),
        account_id=1 # TODO: update once user accounts are implemented
    )
    for cat in data['categories']:
        resto.categories.append(Category.query.filter_by(name=cat).first())

    db.session.add(resto)
    db.session.commit()

    return jsonify({
        'success': True,
    })


@app.route("/api/<int:resto_id>/restaurants", methods=['PATCH'])
def edit_resto(resto_id):
    return jsonify({
        'success': True,
    })


@app.route("/api/<int:resto_id>/restaurants", methods=['DELETE'])
def delete_resto(resto_id):
    return jsonify({
        'success': True,
    })


@app.route("/api/random", methods=['POST'])
def rando_resto():
    return jsonify({
        'success': True
    })
