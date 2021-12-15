from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'id' not in session:
        return render_template("index.html")
    return redirect("/result")

@app.post('/register')
def register():
    if User.is_valid(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "email" : request.form['email'],
            "password" : pw_hash
        }
        id = User.register(data)
        session['id'] = id
        return redirect("/result")
    return redirect('/')

@app.post('/login')
def login():
    user_in_db = User.get_by_email(request.form)

    if not user_in_db:
        flash("Invalid Email/Password",'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email or Password",'login')
        return redirect('/')
    session['id'] = user_in_db.id
    return redirect("/result")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
