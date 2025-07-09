
import requests
from bs4 import BeautifulSoup as bs
from fractions import Fraction
from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Recipe, Ingredient, Step, Users, user_grocery
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from validate_email_address import validate_email



main = Blueprint('main', __name__)


@main.context_processor
def inject_groceries():
    if current_user.is_authenticated:
        recipes = current_user.grocery_recipes.all()
        groceries = [
            {
                'quantity': ing.quantity,
                'unit': ing.unit,
                'name': ing.name
            }
            for recipe in recipes
            for ing in recipe.ingredients
        ]
    else:
        groceries = []
    return dict(groceries=groceries)

def parse_quantity(q):
    try:
        # Handles '1 1/2', '½', etc.
        return float(sum(Fraction(s) for s in q.split()))
    except Exception:
        return None


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@main.route("/")
def home():
    return render_template('index.html')

@main.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("email")
        if not validate_email(username):
            return render_template("sign_up.html", error="Not a Valid email")
        password = request.form.get("password")

        if Users.query.filter_by(username=username).first():
            return render_template("sign_up.html", error="Email already linked to Another account!")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("main.login"))
    if request.method == "GET":
        return render_template("sign_up.html")


@main.route("/login", methods= ['POST', 'GET'])
def login():
    if request.method == 'GET':
       

        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid username or password")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
                    


@main.route("/create-recipe/", methods= ['POST','GET'])
@login_required
def sub():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':


        url = request.form.get('url')  
        str(url)
        r = Recipe.query.filter_by(url=url).first()
        
        if r is None:
            
            parts = url.split(".")
            domain = parts[1]

            if domain == 'allrecipes':
                response = requests.get(url)
                if response.status_code != 200:
                    print("Failed to fetch the page")
                    return None

                soup = bs(response.text, 'html.parser')
                recipeDetails = soup.find_all('ul', class_='mm-recipes-structured-ingredients__list')
                title_tag = soup.find('h1', class_='article-heading text-headline-400')
                title = title_tag.text.strip() if title_tag else 'Untitled'
                r = Recipe(title=title, url=url, user=current_user)
                ingredients = []

                for item in recipeDetails:
                    list_items = item.find_all('li', class_='mm-recipes-structured-ingredients__list-item')
                    for list_item in list_items:
                        # Extract quantity, unit, and name (handle missing elements gracefully)
                        quantity = list_item.find('span', attrs={'data-ingredient-quantity': 'true'})
                        unit = list_item.find('span', attrs={'data-ingredient-unit': 'true'})
                        name = list_item.find('span', attrs={'data-ingredient-name': 'true'})

                        # Get text or empty string if not found
                        quantity_text = quantity.text.strip() if quantity else ''
                        unit_text = unit.text.strip() if unit else ''
                        name_text = name.text.strip() if name else ''

                        # Store as a dictionary or tuple
                        ingredients.append({
                            'quantity': quantity_text,
                            'unit': unit_text,
                            'name': name_text
                        })
                        soup = bs(response.text, 'html.parser')
       
            
                            


                for ing in ingredients:
                                try:
                                    quantity = parse_quantity(ing['quantity']) if ing['quantity'] else None

                                except (ValueError, TypeError):
                                    quantity = None

                                ingredient = Ingredient(
                                    name=ing['name'],
                                    unit=ing['unit'],
                                    quantity=quantity
                                )
                                r.ingredients.append(ingredient)



                



                #directions
        response = requests.get(url)    
        soup = bs(response.text, 'html.parser')

        directions = soup.find_all('p', class_= "comp mntl-sc-block mntl-sc-block-html")
        
        for thing in directions:
            text = thing.get_text(strip=True)
            if not text:
                continue

            step = Step(description=text)
            r.steps.append(step)
                

        db.session.add(r)
        db.session.commit()

        return render_template('recipe.html', recipe=r)        
    
    
@main.route("/bookviewer/", methods=['POST','GET'])
@login_required
def bookviewer():
    if request.method == 'GET':
            recipes = current_user.recipes.all()
            groceries = current_user.grocery_recipes.all()
            return render_template("bookviewer.html", user=current_user, recipes=recipes)
        
    
    
@main.route("/recipe/<int:recipe_id>")
@login_required      
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe.html", recipe=recipe)

@main.route('/recipe-submission/', methods=['POST','GET'])
@login_required
def recipe_submission():
    
    if request.method == 'POST':
        title = request.form.get('title-input')
        quantities = request.form.getlist('quantity-input')
        units      = request.form.getlist('unit-input')
        names      = request.form.getlist('name-input')
        directions = request.form.get('directions-input')
        
        r = Recipe(title=title, url=None, user=current_user)
        
        for qty, unit, name in zip(quantities, units, names):
            if name.strip():  # skip empty rows
                ing = Ingredient(
                    name=name.strip(),
                    quantity=float(qty) if qty else None,
                    unit=unit.strip(),
                    recipe=r
                )
                db.session.add(ing)
        
        db.session.commit()
        
        r.steps.append(Step(description=directions))
        return render_template('recipe.html', recipe = r)
    
    else:
    
        return render_template('recipe_sub.html')
    
@main.route('/add-to-grocery/<int:recipe_id>', methods=['POST'])
@login_required
def addtolist(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user.grocery_recipes.append(recipe)
    db.session.commit()
    return redirect(url_for('main.groceryfetch'))


@main.route('/groceries-fetch', methods=['GET'])
@login_required
def groceryfetch():
    recipes =  current_user.grocery_recipes.all()
    groceries = [
        {
            'name': ing.name,
            'unit': ing.unit,
            'quantity': ing.quantity
        }
        for recipe in recipes
        for ing in recipe.ingredients
    ]
    allrecipes = current_user.recipes.all()
    return render_template(
        'bookviewer.html',
        recipes=allrecipes,
        groceries=groceries
    )
    
@main.route('/grocery-clear', methods=['POST'])
@login_required
def groceryclear():
    db.session.execute(
    user_grocery.delete().where(user_grocery.c.user_id == current_user.id)
)
    db.session.commit()

    return redirect(url_for('main.bookviewer'))