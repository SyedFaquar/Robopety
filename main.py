import bcrypt
from flask import Flask, redirect, url_for, request, render_template, session, jsonify, send_from_directory
from database import get_robots, add_user, validate_user, get_user_robot_by_user, get_user_robot_by_robot, select_pet, return_pet, get_robot_by_id, get_user_by_id
import jwt
import os
import tempfile
from google.cloud import storage
from datetime import datetime, timedelta

app = Flask(__name__)
jwt_secret = os.environ.get('JWT_SECRET')
bucket_name = os.environ.get('BUCKET_NAME')

## home page for robopety
@app.route("/")
def root():
    return redirect(url_for('login'))

## login page
@app.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('login.html')     

## sign up page
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    return render_template('signup.html')

## user page
@app.route('/user/<id>', methods=('GET', 'POST'))
def user(id):
    return render_template('user.html')

## logout function
@app.route('/logout')
def logout():
    return redirect('/')

## user sign up function
@app.route('/usersignup', methods=['POST'])
def usersignup():
    email = request.form.get('email')
    username = request.form.get('username')
    password_1 = request.form.get('password_1')
    password_2 = request.form.get('password_2')
    if not email or not username or not password_1 or not password_2:
        return 'Please fill in all the fields', 401
    if password_1 != password_2:
        return 'Password not matching', 401
    hash_password = hashPassword(password_1)
    response = add_user(email, username, hash_password)
    if response['status'] == 'success':
        data = response['data']
        return getUserInfo(data)
    else:
        return response['error'], 401

## user login function
@app.route('/userlogin', methods=['POST'])
def userlogin():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return 'Please enter an email', 401
    if not password:
        return 'Please enter a password', 401

    response = validate_user(email)
    if response['status'] == 'success':
        data = response['data']
        if bcrypt.checkpw(password.encode('utf-8'), data['password'].encode('utf-8')):
            return getUserInfo(data)
        else:
            return 'Invalid credentials', 401
    else:
        return response['error'], 401

## download the pet image from the google storage
## store in a temp file directory in app engine
## clears out everytime the session ends
@app.route('/getRobotImage/<name>')
def getRobotImage(name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(name)

    with tempfile.TemporaryDirectory() as tmpdirname:
        fullpath = os.path.join(tmpdirname, name)
        blob.download_to_filename(fullpath)
        return send_from_directory(tmpdirname, name)

## Updates the user data
def getUserInfo(data):
    return updateUserRobotData(data['id'])

## Using token from the request body and decode it to obtain user name
@app.route('/getusername', methods=['POST'])
def getUsername():
    token = request.form.get('token')
    try:
        decoded_data = jwt.decode(jwt=token, key=jwt_secret, algorithms='HS256')
        username = decoded_data['username']
        return jsonify({'username': username})
    except jwt.InvalidTokenError:
        return jsonify({'error': "Invalid token"}), 401

## Using token from the request body and decode it to obtain all the available pets
@app.route('/getallrobots', methods=['POST'])
def getAllRobot():
    token = request.form.get('token')
    try:
        decoded_data = jwt.decode(jwt=token, key=jwt_secret, algorithms='HS256')
        robots_list = decoded_data['all_robots']
        user_robot = decoded_data['user_robot']
        all_robots = [item for item in robots_list if item['robot_id'] != user_robot['robot_id']]
        return jsonify({'all_robots': all_robots, 'user_robot': user_robot})
    except jwt.InvalidTokenError:
        return jsonify({'error': "Invalid token"}), 401

## Using token from the request body and decode it to obtain the user robot information 
@app.route('/getuserrobot', methods=['POST'])
def getUserRobot():
    token = request.form.get('token')
    try:
        decoded_data = jwt.decode(jwt=token, key=jwt_secret, algorithms='HS256')
        user_robot = decoded_data['user_robot']
        robot = {'robot': user_robot}
        return jsonify(robot)
    except jwt.InvalidTokenError:
        return jsonify({'error': "Invalid token"}), 401

## Hash function to encrypt the password
def hashPassword(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

## function to set the current robot for user 
@app.route('/setuserrobot', methods=['POST'])
def setUserRobot():
    token = request.form.get('token')
    robot_id = int(request.form.get('robot_id'))
    try:
        decoded_data = jwt.decode(jwt=token, key=jwt_secret, algorithms='HS256')
        user_id = decoded_data['id']
        
        if checkUserRobotAvailability(user_id, robot_id):
            response = select_pet(user_id, robot_id)
            print('Selecting a pet.......', response)
            if response['status'] == 'success':
                return updateUserRobotData(user_id)
            else:
                return jsonify({'error': response['error']}), 401
        else:
            return jsonify({'error': "Something went wrong"}), 401

    except jwt.InvalidTokenError:
        return jsonify({'error': "Invalid token"}), 401

## function for user to return the current robot to the robot store
@app.route('/returnuserrobot', methods=['POST'])
def returnUserRobots():
    token = request.form.get('token')
    robot_id = int(request.form.get('robot_id'))
    try:
        decoded_data = jwt.decode(jwt=token, key=jwt_secret, algorithms='HS256')
        user_id = decoded_data['id']
        print('User is returning a robot.......', user_id, robot_id)
        user_response = get_user_robot_by_user(user_id)
        robot_response = get_user_robot_by_robot(robot_id)
        print('Response from server......', user_response)
        print('Response from robot.......', robot_response)
        if user_response['status'] == 'error':
            return jsonify({'error': user_response['error']})
        if robot_response['status'] == 'error':
            return jsonify({'error': robot_response['error']})
        user_own_robot = user_response['status'] == "success" and user_response['data']['robot_id'] == robot_id and user_response['data']['action'] == 'pick'
        robot_own_by_user = robot_response['status'] == "success" and robot_response['data']['user_id'] == user_id and user_response['data']['action'] == 'pick'
        print('User own robot........', user_own_robot, user_response['status'] == "success", user_response['data']['robot_id'] == robot_id, user_response['data']['action'] == 'pick')
        print('Robot own by user........', robot_own_by_user)
        if user_own_robot and robot_own_by_user:
            print('Return request is sending..........')
            response = return_pet(user_id, robot_id)
            if response['status'] == 'success':
                print('Sending request to the database........')
                return updateUserRobotData(user_id)
            else:
                return jsonify({'error': response['error']}), 401
        return jsonify({'error': 'Something went wrong. Please refresh the page.'}), 401

    except jwt.InvalidTokenError:
        return jsonify({'error': "Invalid token"}), 401

## function to check if current user and current robot are avaible 
def checkUserRobotAvailability(userId, robotId):
    user_response = get_user_robot_by_user(userId)
    robot_response = get_user_robot_by_robot(robotId)
    if user_response['status'] == 'fail':
        return True
    if user_response['status'] == 'success' and user_response['data']['action'] == 'return':
        return True
    if robot_response['status'] == 'fail':
        return True
    if robot_response['status'] == 'success' and user_response['data']['action'] == 'return':
        return True
    return False

## function to retrieve user robot information from database using userId of current user
def updateUserRobotData(userId):
    user_data = get_user_by_id(userId)
    if user_data['status'] == 'fail':
        return jsonify({'error': user_data['error']}), 401
    user_robot_data = get_user_robot_by_user(userId)
    if user_robot_data['status'] == 'success' and user_robot_data['data']['action'] == 'pick':
        robot_id = user_robot_data['data']['robot_id']
        robot_data = get_robot_by_id(robot_id)
        if robot_data['status'] == 'success':
            user_robot = {'robot_id': robot_id, 'robot_name': robot_data['data']['name']}
    else:
        robot_id = -1
        user_robot = {
            'robot_id': robot_id,
            'robot_name': 'None'
        }
    robots_data = get_robots()
    if robots_data['status'] == 'fail':
        return jsonify({'error': robots_data['error']}), 401
    robots = robots_data['data']
    avail_robots = getAvailRobots(robots)
    
    payload = {
        'id': userId,
        'username': user_data['data']['username'],
        'user_robot': user_robot,
        'all_robots': avail_robots
    }
    token = jwt.encode(payload=payload,key=jwt_secret)
    print(token)
    return jsonify({'token': token})

## function to filter all the robots to obtain only the available robot in the store
def getAvailRobots(robots):
    avail_robots = []
    for robot in robots:
        ur_data = get_user_robot_by_robot(robot['id'])
        if ur_data['status'] == 'success' and ur_data['data']['action'] == 'pick':
            continue
        avail_robots.append({'robot_id': robot['id'], 'name':robot['name']})
    return avail_robots

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=False)


