# import flask to create web app + other necessary modules
from flask import Flask, render_template, session, redirect, url_for, flash, request
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

        # activity 2.5 part 1 - add if/else statement to redirect to chat page if valid email, else redirect to index page
        if session['valid_email']:
            return redirect(url_for('chat_page'))
        else:
            return redirect(url_for('index'))
        
    return render_template('index.html', form=form, name = session.get('name'), email = session.get('email'), valid_email = session.get('valid_email')) # pass name/email to index.html

# activity 2.5 part 1 - display chatbot page
@app.route('/chat')
def chat_page():
    return render_template('chat.html')

# activity 2.5 part 2 - add route/remember to chatbot
@app.route('/message', methods=['POST'])
def chat():
    message = request.json["message"]
    # if user says their name, use session to remember
    if "my name is" in message.lower():
        name = message.split("is", 1)[1].strip()
        session['remembered_name'] = name
        reply = "Nice to meet you, " + name + "!"

    # if asked for name, use session to reply with remembered name
    elif "what is my name" in message.lower():
        if 'remembered_name' in session:
            reply = "Your name is " + session['remembered_name'] + "."
        else:
            reply = "I don't know/remember your name yet. Please tell me your name first."

    # extra cases
    elif "hello" in message.lower():
        reply = "Hello!"
    else:
        reply = "I don't understand."

    return {"reply": reply}

# activity 2.5 part 4 - logout and clear session
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)