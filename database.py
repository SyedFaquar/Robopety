import os
import pymysql

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        conn = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    except pymysql.MySQLError as e:
        print(e) 
    return conn


## Retrieve all 50 robots from the database
def get_robots():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT id, name FROM robots')
        robots = cursor.fetchall()
        if result > 0:
            got_robots = {'status':'success', 'data':robots}
        else:
            got_robots = {'status':'fail', 'error':'No robots in DB'}
    conn.close()
    return got_robots

## Validate the email by checking if the email already exists in the database
def validate_user(email):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM users WHERE email = %s', (email))
        user = cursor.fetchall()
        if result > 0:
            got_user = {'status':'success','data':user[0]}
        else:
            got_user = {'status':'fail', 'error': 'Credentials are not correct.'}
    conn.close()
    return got_user

## Retrive user data from the Users table based on the userId
def get_user_by_id(userId):
    conn = open_connection()
    try:
        with conn.cursor() as cursor:
            try:
                result = cursor.execute('SELECT username FROM users WHERE id = %s', (userId))
                user = cursor.fetchall()
                if result > 0:
                    response =  {'status': 'success', 'data': user[0]}
                else:
                    response = {'status': 'fail', 'error': 'Something went wrong'}
            except pymysql.Error as e:
                conn.rollback()
                response = {'status': 'fail', 'error': e}
    except pymysql.Error as e:
        response = {'status':'fail', 'error':e}
    conn.close()
    return response

## Retrieve user
def get_robot_by_id(robotId):
    conn = open_connection()
    try:
        with conn.cursor() as cursor:
            try:
                result = cursor.execute('SELECT name FROM robots WHERE id = %s', (robotId))
                robot = cursor.fetchall()
                if result > 0:
                    response =  {'status': 'success', 'data': robot[0]}
                else:
                    response = {'status': 'fail', 'error': 'Something went wrong'}
            except pymysql.Error as e:
                conn.rollback()
                response = {'status': 'fail', 'error': e}
    except pymysql.Error as e:
        response = {'status':'fail', 'error':e}
    conn.close()
    return response

## Insert a new user into the User table
def add_user(email, username, password):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT COUNT(*) as count FROM users WHERE email = %s', email)
        count = cursor.fetchall()
        if count[0]['count'] > 0:
            user =  {'status':'fail', 'error': "email already used"}
        else: 
            cursor.execute('INSERT INTO users (email, username, password) VALUES(%s, %s, %s)', (email, username, password))
            conn.commit()
            user = validate_user(email)
    conn.close()
    return user 

## Retrieve all user information from the Users table
def get_users():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        if result > 0:
            got_users = {'status':'success', 'data':users}
        else:
            got_users = {'status':'failed', 'error': 'empty database'}
    conn.close()
    return got_users

## Retrive the current robot of the user with userId
def get_user_robot_by_user(userid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM user_robots WHERE user_id = %s ORDER BY id DESC LIMIT 1', userid)
        robot = cursor.fetchall()
        if result > 0:
            got_robot = {'status':'success', 'data':robot[0]}
        else:
            got_robot = {'status':'fail', 'error':'User does not have a robot'}
    conn.close()
    return got_robot

## Retrive the current user of the robot with robotId
def get_user_robot_by_robot(robotid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM user_robots WHERE robot_id = %s ORDER BY id DESC LIMIT 1', robotid)
        robot = cursor.fetchall()
        if result > 0:
            got_robot = {'status':'success', 'data':robot[0]}
        else:
            got_robot = {'status':'fail', 'error':'No one picked this robot'}
    conn.close()
    return got_robot

## Insert a transcation to the User_Robots table to indicate that 
## User with UserId has selected robot with RobotId
def select_pet(userId, robotId):
    conn = open_connection()
    try:
        with conn.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO user_robots (user_id, robot_id, action) VALUES(%s, %s, %s)', (userId, robotId, "pick"))
                conn.commit()
                num_affected_rows = cursor.rowcount
                if num_affected_rows > 0:
                    conn.close()
                    return {'status': 'success', 'data': num_affected_rows}
                else:
                    conn.close()
                    return {'status': 'fail', 'error': 'Something went wrong'}
            except pymysql.Error as e:
                conn.rollback()
                conn.close()
                return {'status': 'error', 'error': e}
    except pymysql.Error as e:
        conn.close()
        return {'status':'error', 'error':e}

## Insert a transaction into the User_Robot Table indicate that
## User with userId has returned robot with RobotID
def return_pet(userId, robotId):
    conn = open_connection()
    try:
        with conn.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO user_robots (user_id, robot_id, action) VALUES(%s, %s, %s)', (userId, robotId, "return"))
                conn.commit()
                num_affected_rows = cursor.rowcount
                if num_affected_rows > 0:
                    conn.close()
                    return {'status': 'success', 'data': num_affected_rows}
                else:
                    conn.close()
                    return {'status': 'fail', 'error': 'Something went wrong'}
            except pymysql.Error as e:
                conn.rollback()
                conn.close()
                return {'status': 'error', 'error': e}
            
    except pymysql.Error as e:
        conn.close()
        return {'status':'error', 'error':e}