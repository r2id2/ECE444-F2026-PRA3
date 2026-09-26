# 2-1: Basic Routing
# import flask to create web app
from flask import Flask, render_template # lets flask display HTML files from templates folder
from flask_bootstrap import Bootstrap # to style HTML files
from flask_moment import Moment # to display time in HTML files
from datetime import datetime # to get current time

# make and connect flask app to bootstrap and moment
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# route to display index.html when user goes to root URL
@app.route('/')
def index():
    return render_template('index.html', name='Raida Fardous', current_time=datetime.utcnow())

# 2-2: Dynamic Routing
# route to display user.html when user goes to /user/<name> URL
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

# error handlers - if user requests a page that does not exist, display 404.html
# if there is an internal server error, display 500.html
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500