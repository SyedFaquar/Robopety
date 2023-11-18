import datetime

from flask import Flask, redirect, url_for, request, render_template, session
from db import db

app = Flask(__name__)

## home page for robopety
@app.route("/")
def root():
    return render_template("login.html")

## login page
@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if email is None or email != db()['email'] or  password != db()['password']:
            error = 'You have entered an incorrect email or password.'
        
        if error is None:
            ## session.clear()
            session['username'] = email
            return redirect(url_for('user'))
        
        ##flash(error)
    return render_template('login.html', error = error)    

## sign up page
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password_1 = request.form['password_1']
        password_2 = request.form['password_2']
        

        if not email:
            error = 'Username is required.'
        elif not password_1:
            error = "Password is required."
        elif not password_2:
            error = "Password Confirmation is required."

        if error is None:
            if email == db()['email']:
                error = 'Email is already used.'
            elif password_1 != password_2:
                error = 'Passwords are not matching.'
            else:
                session['username'] = email
                return redirect(url_for('user'))
        ##flash(error) 
    return render_template('signup.html', error = error)

## user page
@app.route('/user', methods=('GET', 'POST'))
def user():
    username = session.get('username', None)
    return render_template('user.html', username=username)

## logout function
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.secret_key = 'super secret key'

    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)