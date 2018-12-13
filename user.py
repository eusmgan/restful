import sqlite3
from flask_restful import Resource, reqparse
from flask import render_template, session
import psycopg2
from flask import make_response
from werkzeug.security import safe_str_cmp

class User(Resource):
    TABLE_NAME = 'users'

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):

        conn_string = "host='127.0.0.1' dbname='parcelflow' user='postgres' password='postgres'"

        # print the connection string we will use to connect
        print "Connecting to database\n ->%s" % (conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        #username = request.form['username']
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username='" + username + "'"
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserLogin(Resource):

    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = UserRegister.parser.parse_args()

        user = User.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            session['logged_in'] = True
        else:
            return {"message": "Invalid Credentials!"}, 401
        return render_template('home.html')


class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        print 'username1' + data['username']
        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        conn_string = "host='localhost' dbname='parcelflow' user='postgres' password='postgres'"

        # print the connection string we will use to connect
        print "Connecting to database\n ->%s" % (conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        query = "INSERT INTO users (id, username, password ) VALUES (DEFAULT, '" + data['username'] + "', '" +  data['password'] + "')"
        cursor.execute(query)

        conn.commit()
        conn.close()

        resp=make_response(render_template('home.html', username=data['username']))
        resp.headers.extend({'Content-Type': 'text/html'})
        return resp

       # return {"message": "User created successfully."}, 201
