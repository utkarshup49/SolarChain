"""
This file has the forms for our flask website
"""

# Import necessary components for form handling in Flask
from flask_wtf import FlaskForm  # Base class for creating secure web forms
from wtforms import StringField, PasswordField, SubmitField, BooleanField  # Standard input fields
from wtforms.fields.numeric import IntegerField  # Numeric input field
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange  # Validation utilities

from main.models import User  # Import the User model for database interaction

# Form for user registration with fields for username, password, and password confirmation
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])  # Username field with length constraints
    password = PasswordField('Password', validators=[DataRequired()])  # Password field (input hidden)
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])  # Password confirmation
    submit = SubmitField('Sign Up')  # Submit button

    # Custom validation to check if the username already exists in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()  # Check for existing username
        if user:
            raise ValidationError("Username is already taken, please choose another name.")  # Error if username exists


# Form for user login with fields for username, password, and a 'remember me' option
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Username field
    password = PasswordField('Password', validators=[DataRequired()])  # Password field (input hidden)
    remember = BooleanField('Remember Me')  # Checkbox to remember user session
    submit = SubmitField('Login')  # Submit button


# Form for creating a sell order with fields for units and price per unit
class SellOrderForm(FlaskForm):
    unit = IntegerField('Units', validators=[DataRequired()])  # Number of units to sell
    price = IntegerField('Price Per unit', validators=[DataRequired()])  # Price per unit
    submit = SubmitField('Sell Units')  # Submit button


# Form for purchasing units with validation for non-negative numbers
class PurchaseForm(FlaskForm):
    units = IntegerField('Units', validators=[DataRequired(), NumberRange(0)])  # Units to purchase (must be >= 0)
    submit = SubmitField('Buy')  # Submit button
