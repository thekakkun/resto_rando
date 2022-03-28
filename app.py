import os

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import Category, db

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/resto_rando'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/categories", methods=['GET'])
def get_categories():
    categories = Category.query.all()

    return jsonify({
        'success': True,
        "categories": {cat.id: cat.name for cat in categories}
    })
