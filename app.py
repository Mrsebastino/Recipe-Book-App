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
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

""" This is the route to the homepage
    it will only be used as a link from the Home Cooking logo
"""


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", page_title="What's Cooking?")


"""
Route to  existing recipe and added recipe by user
"""
# provide all recipes from DB


@app.route('/our_recipes')
def our_recipes():
    all_recipes = mongo.db.recipes.find()

    return render_template("our_recipes.html",
                           recipes=all_recipes,
                           )


"""
 Route to  add recipe form.
"""
# Allow the user to add their recipe


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


@app.route('/your_recipes/<recipe_id>')
def your_recipes(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

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
    equipments_use = request.form.getlist("equipment_name")

    ingredients_list = form_data["ingredients_name"].split("\n")
    instructions_list = form_data["instructions_name"].split("\n")
    equipments_list = equipments_use
    the_recipe = recipes.insert_one(
        {
            "category_name": form_data["category_name"],
            "recipe_name": form_data["recipe_name"],
            "difficulty_name": form_data["difficulty_name"],
            "serve_name": form_data["serve_name"],
            "ingredients_name": ingredients_list,
            "instructions_name": instructions_list,
            "equipment_name": equipments_list,
            "image_link": form_data["image_link"]

        }
    )

    return redirect(url_for("your_recipes", recipe_id=the_recipe.inserted_id))


"""
 Route to Edit recipe page
"""


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_recipes = mongo.db.recipes.find()
    all_categories = mongo.db.categories.find()
    all_equipments = mongo.db.equipments.find()

    return render_template("edit_recipes.html",
                           recipe=the_recipe,
                           recipes=all_recipes,
                           categories=all_categories,
                           equipments=all_equipments,
                           page_title="Edit Recipe"
                           )


"""
 Route to update recipe
"""


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    form_data = request.form.to_dict()
    equipments_use = request.form.getlist("equipment_name")

    ingredients_list = form_data["ingredients_name"].split("\n")
    instructions_list = form_data["instructions_name"].split("\n")
    equipments_list = equipments_use
    recipes.update(
        {"_id": ObjectId(recipe_id)},

        {
            "category_name": form_data["category_name"],
            "recipe_name": form_data["recipe_name"],
            "difficulty_name": form_data["difficulty_name"],
            "serve_name": form_data["serve_name"],
            "ingredients_name": ingredients_list,
            "instructions_name": instructions_list,
            "equipment_name": equipments_list,
            "image_link": form_data["image_link"]

        })
    return redirect(url_for("our_recipes",
                            recipe_id=recipe_id
                            ))


"""
Route to delete selected recipe from DB
"""


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('our_recipes'))


"""
Route to equipments page
"""


@app.route('/equipments_list')
def equipments_list():
    recipes = mongo.db.recipes.find()
    all_equipments = list(mongo.db.equipments.find())

    return render_template("equipment.html",
                           recipes=recipes,
                           equipments=all_equipments
                           )


"""
Route to view recipe linked to the equipment selected
by user.
"""


@app.route('/recipes_by_equipment/<equipment_name>')
def recipes_by_equipment(equipment_name):
    recipes = mongo.db.recipes.find(
        {'equipment_name': {'$in': [equipment_name]}},
    ).limit(5)

    return render_template('our_recipes.html', recipes=recipes)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
