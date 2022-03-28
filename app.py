from flask import Flask
from flask_migrate import Migrate
import os

from models import db

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres://{DB_USER}:{DB_PASSWORD}@localhost:5432/resto_rando'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
