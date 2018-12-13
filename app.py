from flask import Flask, render_template, request, redirect, url_for, session
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister, UserLogin, User
from item import Item, ItemList






#  return app.send_static_file('index.html')






app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

#username = request.form['username']
#password = request.form['password']
#user = UserSignup(username,password)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

@app.route('/register')
def signup():
    error = None
    if request.method == 'POST':
     username = request.form['username']
     password = request.form['password']
     user = UserRegister(username,password)
     return app.send_static_file('index.html')
    return app.send_static_file('index.html')

@app.route('/login')
def login():
    error = None
    if request.method == 'POST':
     username = request.form['username']
     password = request.form['password']
     user = UserLogin(username,password)
     session['logged_in'] = True
     return render_template('index.html')
    return app.send_static_file('index.html')


@app.route('/logout')
def logout():
    error = None
    session['logged_in'] = False
    return "Logged out"

@app.route('/')
def home():
    if not session.get('logged_in'):
        return login()
    else:
        return app.send_static_file('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0')

