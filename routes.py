from flask import Flask, render_template, request
from models import Recipe, Step, Ingredient
from app import app
import requests
from bs4 import BeautifulSoup as bs
from app import db



@app.route("/")
def home():
    return render_template('index.html')
    

@app.route("/submit/", methods= ['POST','GET'])
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
        
