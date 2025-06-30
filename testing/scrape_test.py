import requests
from bs4 import BeautifulSoup as bs

def scrape(url):
    print(url)
    parts = url.split(".")
    domain = parts[1]

    if domain == 'allrecipes':
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to fetch the page")
            return None

        soup = bs(response.text, 'html.parser')
        directions = soup.find_all('p', class_= "comp mntl-sc-block mntl-sc-block-html")
        
        for thing in directions:
            print(thing.text.strip())
# Example usage:
ingredients = scrape('https://www.allrecipes.com/recipe/14211/macaroni-salad-with-pickles/')

