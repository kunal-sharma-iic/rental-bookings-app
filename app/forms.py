from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import InputRequired, Email, Length
         
 
""" class for login form validation"""

class LoginForm(FlaskForm):
    email = StringField("Email",  [InputRequired("Please enter email address"), Email(message = "Please enter a valid email address"), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=60)])
 
 
"""class for signup form validation"""
 
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired("Please enter your name"), Length(min=3, max=20)])
    email = StringField("Email",  [InputRequired("Please enter email address"), Email(message = "Please enter a valid email address"), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=60)])
 