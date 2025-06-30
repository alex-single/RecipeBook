from . import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), unique=True, nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', cascade='all, delete-orphan', lazy='dynamic')
    steps = db.relationship('Step', backref='recipe', cascade='all, delete-orphan', lazy='dynamic')

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(128))

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10000), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
