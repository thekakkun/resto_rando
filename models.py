from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    restaurants = db.relationship('Restaurant', backref='user', lazy=True)


restaurant_category = db.Table(
    'restaurant_category',
    db.Column('restaurant_id', db.Integer, db.ForeignKey(
        'restaurant.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey(
        'category.id'), primary_key=True)
)


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=True)
    address = db.Column(db.String(160), nullable=True)
    visited = db.Column(db.Boolean, default=False, nullable=False)
    date_visited = db.Column(db.Date, nullable=True)
    categories = db.relationship('Category', secondary=restaurant_category,
                                 lazy='subquery', backref=db.backref('restaurants', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
