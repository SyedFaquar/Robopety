import datetime
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, url_for, request, render_template, session, jsonify
from db import db, get_db_pet

app = Flask(__name__)

## home page for robopety
@app.route("/")
def root():
    return redirect(url_for('login'))

## login page
@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if email is None or email != db()['email'] or password != db()['password']:
            error = 'You have entered an incorrect email or password.'
        
        if error is None:
            ## session.clear()
            session['username'] = email
            return redirect(url_for('user',id=1))
        
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
                return redirect(url_for('user', id=1))
        ##flash(error) 
    return render_template('signup.html', error = error)

## user page
@app.route('/user/<id>', methods=('GET', 'POST'))
def user(id):
    username = session.get('username', None)
    if not username:
        return redirect(url_for('login'))
    pets = get_db_pet()
    currentPet = session.get('current_pet', None)
    if currentPet:
        pets = [item for item in pets if currentPet['name'] != item['name']]
    return render_template('user.html', username=username, currentPet=currentPet, pets=pets)

@app.route('/setpet', methods=['POST'])
def setPet():
    username = session.get('username', None)
    currentPet = session.get('current_pet', None)
    if currentPet:
        pets = [item for item in get_db_pet() if item['name'] != currentPet['name']]
        return render_template('user.html', username=username, currentPet=currentPet, pets=pets)
    currentPetName = request.form.get('data_from_button')
    pets = []
    for item in get_db_pet():
        if item['name'] != currentPetName:
            pets.append(item)
        else:
            currentPet = item
            session['current_pet'] = item
    print(pets, currentPet)
    return render_template('user.html', username=username, currentPet=currentPet, pets=pets)

## filter pets
@app.route('/filtered/<filter_value>')
def filter_list(filter_value):
    pets = get_db_pet()
    currentPet = session.get('current_pet', None)
    if filter_value != 'None':
        filtered_pets = [item for item in pets if filter_value.lower() in item['name'].lower()]
    else:
        filtered_pets = pets
    if currentPet:
        filtered_pets = [item for item in filtered_pets if currentPet['name'] != item['name']]
    return jsonify(filtered_list=filtered_pets, currentPet=currentPet)

## return pets
@app.route('/returnpet')
def returnPet():
    username = session.get('username', None)
    session['current_pet'] = None
    pets = get_db_pet()
    return render_template('user.html', username=username, currentPet=None, pets=pets)
    


## logout function
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    

if __name__ == "__main__":
    app.secret_key = os.getenv('FLASK_SECRET_KEY')

    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)


