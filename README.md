#  Recipe Box
### A place for users to find, save, and take notes for recipes
See it in action here: https://rb-recipebox.herokuapp.com/

Or set it up for yourself:
1. Create a `config.py` file on the same level as the `app.py` file. 
2. Get an API key from Spoonacular API and save it as `APIKEY` in the `config.py`
3. Create a database named 'recipebox' to connect to with postgres

## Overview
Recipe Box is a place for users to find new recipes - either generally or with ingredient filters. Registered users can save recipes to their recipe box and save notes.

### Recipe Search
Both advanced and basic recipe search is accessible to non-logged-in users. Basic recipe search occurs from the nav bar. Advanced Recipe Search routes to a form that allows the user to include/exclude ingredients, select a Diet type (e.g. Keto, Whole30, Paleo, Mediterranean, etc.), and a max cooking time.  

### Create an account
Kept this to the basics - no profile picture needed; the user's email doubles as a login credential. The user can also save their allergens and those ingredients won't be in resulting recipe searches.

### Saved Recipes
All saved recipes are listed on a single page, with notes that are easy to edit.

### Recipe Info
The Recipe Information page shows detailed information for a recipe- # of servings, ingredients, and instructions - as well as the original source or the recipe (e.g. Bon Appetit, Serious Eats, Simply Recipes, etc.) 

At the bottom, there are also similar recipe titles to check out

## Walk Through
1. Create an account
2. Search for Recipes (from the nav bar or Advanced Search link)
3. Browse and save recipes - it comes back to the Saved Recipes page so it's easy to quickly add a note

#### Technologies used
:: Python, Flask, PostgreSQL, Javascript, HTML, CSS, Bootstrap

