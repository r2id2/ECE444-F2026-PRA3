# 2-1: Basic Routing
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

# 2-2: Dynamic Routing
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)