from flask import Flask, render_template, request, redirect, url_for
from models import Recipe, Step, Ingredient, Users
from app import app
import requests
from bs4 import BeautifulSoup as bs
from app import db, login_manager, check_password_hash, login_user,generate_password_hash,logout_user, login_required



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        if Users.query.filter_by(username=username).first():
            return render_template("sign_up.html", error="Username already taken!")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    if request.method == "GET":
        return render_template("sign_up.html")


@app.route("/login", methods= ['POST', 'GET'])
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
                    


@app.route("/create-recipe/", methods= ['POST','GET'])
def sub():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':


        url = request.form.get('url')  
        str(url)
        r = Recipe.query.filter_by(url=url).first()
        
        if r is None:
            
            print(url)
            parts = url.split(".")
            domain = parts[1]
            
            #allrecipes https://www.allrecipes.com/
            if domain == 'allrecipes' :
                
                
                
                #driver.get(url)
                response = requests.get(url)
            
                # Check if the request was successful
                if response.status_code != 200:
                    print("Failed to fetch the page")
                    return None

                # Parse the HTML content
                soup = bs(response.text, 'html.parser')
                recipeDetails = soup.find_all('ul', class_ = 'mm-recipes-structured-ingredients__list')
                ingredients = []
            
                for item in recipeDetails:
                    list_items = item.find_all('li', class_='mm-recipes-structured-ingredients__list-item')
                    for list_item in list_items:
                        name = list_item.find('span', attrs={'data-ingredient-name': 'true'}).text.strip()
                        ingredients.append(name)
                        
                        #note to self ^^ strip after commas on the stupid shit

                        
                cleaned_ingredients = []
                for ingredient in ingredients:
                    if ',' in ingredient:
                        clean_ingredient = ingredient.split(',')
                        cleaned_ingredients.append(clean_ingredient[0])
                    else:
                        cleaned_ingredients.append(ingredient)
                    

                r = Recipe(title='hi', url=url)

                for name in cleaned_ingredients:
                    r.ingredients.append(Ingredient(name=name))
                
                db.session.add(r)
                db.session.commit()

        return render_template('recipe.html', recipe=r)        
        
