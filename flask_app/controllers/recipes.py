from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)


@app.route('/result')
def result():
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': session['id']
    }
    results = User.get_by_id(data)
    recipes = Recipe.get_recipe()
    print(results)
    return render_template("dashboard.html", results=results, recipes=recipes)

@app.route("/to_create")
def to_create_recipe():
    if 'id' not in session:
        return redirect('/')
    return render_template ("add_recipe.html")

@app.post('/create')
def create_recipe():
    if 'id' not in session:
        return redirect('/')
    if Recipe.is_valid(request.form):
        data = {
            'user_id': session['id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'time': request.form['time'],
            'instruction': request.form['instruction'],
            'date_made_on': request.form['date_made_on'],
        }
        Recipe.create_recipe(data)
        return redirect("/result")
    return redirect('/to_create')

@app.route("/to_edit/<int:id>")
def to_edit_recipe(id):
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    recipes = Recipe.get_one_recipe(data)
    if recipes.user_id == session['id']:
        return render_template("edit_recipe.html", recipes=recipes)
    return redirect('/')

@app.post('/edit/<int:id>')
def edit_recipe(id):
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': id,
        **request.form
    }
    Recipe.edit_recipe(data)
    return redirect("/result")


@app.route('/delete/message/<int:id>')
def delete_message(id):
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': id,
    }
    recipes = Recipe.get_one_recipe(data)
    if recipes.user_id == session['id']:
        Recipe.delete_message(data)
        return redirect("/result")
    return redirect('/')

@app.route("/to_show/<int:id>")
def to_show(id):
    if 'id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    data2 = {
        "id": session['id']
    }
    recipes = Recipe.get_one_recipe(data)
    results = User.get_by_id(data2)
    return render_template("recipes.html", recipes = recipes, results = results)


