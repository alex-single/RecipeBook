from app import db
from app import UserMixin
#AUTH

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)









class Recipe(db.Model):

    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), unique=True, nullable=False)
    time_created = db.Column(db.DateTime, server_default=db.func.now())

    ingredients = db.relationship(

        'Ingredient',
        backref='recipe',
        cascade='all, delete-orphan',
        lazy='dynamic'

    )

    steps = db.relationship(
        
        'Step',
        backref='recipe',
        cascade='all, delete-orphan',
        lazy='dynamic'                    
                            
                            
    
    
    
    )

class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(128), nullable=False)
    recipe_id  = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)


class Step(db.Model):
    __tablename__ = "step"

    id           = db.Column(db.Integer, primary_key=True)
    step_number  = db.Column(db.Integer, nullable=False)
    description  = db.Column(db.Text, nullable=False)
    recipe_id    = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)