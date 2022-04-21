from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

# TODO: Create methods for common actions (add, delete, etc.)


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    restaurants = db.relationship('Restaurant', backref='account', lazy=True)


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
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    def out(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'visited': self.visited,
            'date_visited': self.date_visited,
            'categories': [cat.name for cat in self.categories],
            'account_id': self.account_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


def populate_cat():
    with open('categories.csv', 'r') as f:
        cats = f.read().split('\n')
        for cat_name in cats:
            db.session.add(Category(name=cat_name))
        db.session.commit()


def insert_dummy_data():
    populate_cat()

    db.session.add(Account(id=1, name='auth0|6250692a17abb90069efb4a2'))
    db.session.add(Account(id=2, name='auth0|6250694cfa08af006b866c9f'))

    db.session.commit()

    db.session.add(Restaurant(
        name='Best Restaurant',
        address='123 Main Street, New York, NY',
        categories=[
            Category.query.filter_by(name='African').first(),
            Category.query.filter_by(name='Vegan').first()
        ],
        visited=True,
        account_id=1
    ))
    db.session.add(Restaurant(
        name='Foo Foods',
        address='123 Pacific Drive, Los Angeles, CA',
        categories=[
            Category.query.filter_by(name='Asian').first(),
            Category.query.filter_by(name='Fast Food').first()
        ],
        visited=False,
        account_id=1
    ))

    db.session.commit()
