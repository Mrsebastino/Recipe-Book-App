import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId

# DB URI for local workspace
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipe_book'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

# Route to Home page


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", recipes=mongo.db.recipes.find(),       page_title="What's Cooking?")

# Route to  exixting recipe


@app.route('/our_recipes')
def our_recipes():
    the_recipe = mongo.db.recipes.find()

    return render_template('our_recipes.html', recipes=the_recipe)

# Route to  add recipe form


@app.route('/add_recipes')
def add_recipes():
    return render_template("add_recipes.html", recipes=mongo.db.recipes.find(),   categories=mongo.db.categories.find(), page_title="Add Recipe")

# Route to new added recipe


@app.route('/your_recipes/<recipes_id>')
def your_recipes(recipes_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipes_id)})
    return render_template("your_recipes.html", recipes=the_recipe, page_title="Your Recipe")

# Route to take our data from ad recipe form and display in your recipe


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    form_data = request.form.to_dict()

    ingredients_list = form_data["ingredients_name"].split("\n")
    instructions_list = form_data["instructions_name"].split("\n")

    the_recipe = recipes.insert_one(
        {
            "category_name": form_data["category_name"],
            "recipe_name": form_data["recipe_name"],
            "difficulty_name": form_data["difficulty_name"],
            "serve_name": form_data["serve_name"],
            "ingredients_name": ingredients_list,
            "instructions_name": instructions_list,
            "image_link": form_data["image_link"]

        }
    )

    return redirect(url_for('your_recipes', recipes_id=the_recipe.inserted_id))


@app.route('/equipments_list')
def equipments_list():
    all_equipments = mongo.db.equipments.find()
    return render_template("equipment.html", equipments=all_equipments)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
