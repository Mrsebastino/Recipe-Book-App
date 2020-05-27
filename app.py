import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId

""" DB URI for local workspace
"""
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipe_book'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

""" This is the route to the homepage
    it will only be used as a link from the Home Cooking logo
"""


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", page_title="What's Cooking?")


"""
Route to  exixting recipe and added recipe by user
"""


@app.route('/our_recipes')
def our_recipes():
    all_recipes = mongo.db.recipes.find()
    all_categories = mongo.db.categories.find()
    all_equipments = mongo.db.equipments.find()

    return render_template("our_recipes.html",
                           recipes=all_recipes,
                           equipments=all_equipments,
                           categories=all_categories
                           )


"""
 Route to  add recipe form. Allow the user to add their recipe
"""


@app.route('/add_recipes')
def add_recipes():
    all_recipes = mongo.db.recipes.find()
    all_categories = mongo.db.categories.find()
    all_equipments = mongo.db.equipments.find()
    return render_template("add_recipes.html",
                           recipes=all_recipes,
                           categories=all_categories,
                           equipments=all_equipments,
                           page_title="Add Recipe"
                           )


"""
 Route to new added recipe
 Redirect the user to their added recipe
"""


@app.route('/your_recipes/<recipes_id>')
def your_recipes(recipes_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipes_id)})
    return render_template("your_recipes.html",
                           recipes=the_recipe,
                           page_title="Your Recipe"
                           )


"""
 Route to take our data from add recipe form
 and display it in your_recipe page
"""


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    form_data = request.form.to_dict()

    ingredients_list = form_data["ingredients_name"].split("\n")
    instructions_list = form_data["instructions_name"].split("\n")
    equipments_list = form_data["equipments_name"].split("\n")
    the_recipe = recipes.insert_one(
        {
            "category_name": form_data["category_name"],
            "recipe_name": form_data["recipe_name"],
            "difficulty_name": form_data["difficulty_name"],
            "review_name": form_data["review_name"],
            "serve_name": form_data["serve_name"],
            "ingredients_name": ingredients_list,
            "instructions_name": instructions_list,
            "equipments_name": equipments_list,
            "image_link": form_data["image_link"]

        }
    )

    return redirect(url_for("your_recipes", recipes_id=the_recipe.inserted_id))


"""
 Route to Edit recipe page
"""


@app.route('/edit_recipe/<recipes_id>')
def edit_recipe(recipes_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipes_id)})
    all_recipes = mongo.db.recipes.find()
    all_equipments = mongo.db.equipments.find()
    all_categories = mongo.db.categories.find()

    return render_template("edit_recipes.html",
                           recipe=the_recipe,
                           recipes=all_recipes,
                           equipments=all_equipments,
                           categories=all_categories,
                           page_title="Edit Recipe"
                           )


@app.route('/update_recipe/<recipes_id>',  methods=["POST"])
def update_recipe(recipes_id):
    recipes = mongo.db.recipes
    form_data = request.form.to_dict()

    ingredients_list = form_data["ingredients_name"].split("\n")
    instructions_list = form_data["instructions_name"].split("\n")
    equipments_list = form_data["equipments_name"].split("\n")
    recipes.update(
        {"_id": ObjectId(recipes_id)},
        {
            "category_name": form_data["category_name"],
            "recipe_name": form_data["recipe_name"],
            "difficulty_name": form_data["difficulty_name"],
            "review_name": form_data["review_name"],
            "serve_name": form_data["serve_name"],
            "ingredients_name": ingredients_list,
            "instructions_name": instructions_list,
            "equipments_name": equipments_list,
            "image_link": form_data["image_link"]

        })
    return redirect(url_for("our_recipes"))


@app.route('/delete_recipe/<recipes_id>')
def delete_recipe(recipes_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipes_id)})
    return redirect(url_for('our_recipes'))


@app.route('/equipments_list')
def equipments_list():
    all_equipments = mongo.db.equipments.find()
    return render_template("equipment.html", equipments=all_equipments)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
