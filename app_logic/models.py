from . import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    recipes = db.relationship(
        'Recipe',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), unique=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(
        'Users',
        back_populates='recipes'
    )
    ingredients = db.relationship(
        'Ingredient',
        back_populates='recipe',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
    steps = db.relationship(
        'Step',
        back_populates='recipe',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(128))
    recipe = db.relationship('Recipe', back_populates='ingredients')


class Step(db.Model):
    __tablename__ = 'steps'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10000), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='steps')