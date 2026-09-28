# import flask to create web app + other necessary modules
from flask import Flask, render_template, session, redirect, url_for, flash 
from flask_bootstrap import Bootstrap # to style HTML files

# for forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

# make form 
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your email?', validators=[DataRequired(), Email()]) # to verify email format
    submit = SubmitField('Submit')

# make and connect flask app to bootstrap 
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

# route to display index.html when user goes to root URL
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit(): # check if form valid
        ## yellow boxes for name and email if user submits diff values
        # check if name changed from prev submission
        if session.get('name') is not None \
                and session.get('name') != form.name.data:
            flash('Looks like you have changed your name!')

        # check if the email changed from prev submission
        if session.get('email') is not None \
                and session.get('email') != form.email.data:
            flash('Looks like you have changed your email!')

        # save the new name/email
        session['name'] = form.name.data
        session['email'] = form.email.data

        # check for valid email
        if 'utoronto' in form.email.data.lower():
            # valid UofT email            
            session['valid_email'] = True
        else:
            # not a UofT email
            session['valid_email'] = False
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name = session.get('name'), email = session.get('email'), valid_email = session.get('valid_email')) # pass name/email to index.html

# run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)