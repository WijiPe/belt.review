from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'id' not in session:
        return render_template("index.html")
    return redirect("/result/")

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
        return redirect("/result/")
    return redirect('/')

@app.route('/result/')
def result():
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': session['id']
    }
    results = User.get_by_id(data)
    messages = Message.get_message(data)
    users = User.get_all()
    print(results)
    return render_template("result.html", results=results, messages=messages, users=users)

@app.post('/login')
def login():
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password",'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email or Password",'login')
        return redirect('/')
    session['id'] = user_in_db.id
    return redirect("/result/")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/destroy/message/<int:id>')
def destroy_message(id):
    data = {
        'id': id
    }
    check_id = Message.get_message_by_id(data)
    if check_id.receiver_id == session['id']:
        Message.destroy_message(data)
        return redirect('/result/')
    return render_template("delete_message.html", id=id)

@app.post('/send/message')
def send_message():
    data = {
        'message': request.form["message"],
        'sender_id': session['id'],
        'receiver_id': request.form['receiver_id']
    }
    Message.save_message(data)
    return redirect("/result/")
