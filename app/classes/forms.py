# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask.app import Flask
from flask import flash
from flask_wtf import FlaskForm
from mongoengine.fields import EmailField
import mongoengine.errors
from wtforms.validators import URL, NumberRange, Email, Optional, InputRequired, ValidationError, DataRequired, EqualTo
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, HiddenField, IntegerField, SelectField, FileField, BooleanField
from app.classes.data import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField()
    #role = SelectField('Role', choices = [("Teacher", "Teacher"), ("Student", "Student")])
    #favColor = SelectField('Favorite Color', choices = [("Blue", "Blue"), ("Yellow", "Yellow")])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])  
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        try:
            User.objects.get(username=username.data)
        except mongoengine.errors.DoesNotExist:
            flash(f"{username.data} is available.")
        else:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        try:
            User.objects.get(email=email.data)
        except mongoengine.errors.DoesNotExist:
            flash(f'{email.data} is a unique email address.')
        else:
            raise ValidationError('This email address is already in use. if you have forgotten your credentials you can try to recover your account.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')
    #favColor = SelectField('Favorite Color', choices = [("Blue", "Blue"), ("Yellow", "Yellow")])
    proc = SelectField('Type of Procrastinator', choices = [("Super Procrastinator", "Super Procrastinator"), ("Procrastinator", "Procrastinator"), ("Jeff Bezos Delivery", "Jeff Bezos Delivery")])
    procrastinatedTime = SelectField('Time Procrastinated', choices = [("1  Hours", "1  Hours"), ("2 Hours", "2 Hours"), ("3 Hours", "3 Hours"), ("4 Hours", "4 Hours"), ("5 Hours", "5 Hours"), ("6 Hours", "6 Hours"), ])

#To record time procrastinated and time worked
class TimeProcForm(FlaskForm):
    proc = SelectField('Type of Procrastinator', choices = [("Super Procrastinator", "Super Procrastinator"), ("Procrastinator", "Procrastinator"), ("Jeff Bezos Delivery", "Jeff Bezos Delivery")])
    procrastinatedTime = SelectField('Time Procrastinated', choices = [("1  Hours", "1  Hours"), ("2 Hours", "2 Hours"), ("3 Hours", "3 Hours"), ("4 Hours", "4 Hours"), ("5 Hours", "5 Hours"), ("6 Hours", "6 Hours"), ])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Post', validators=[DataRequired()])
    submit = SubmitField('Post')
    postType = SelectField('Type of Post', choices = [("Based", "Based"), ("Requests", "Requests"), ("Demands", "Demands"), ("Help Me", "Help Me")])

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')