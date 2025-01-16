"""
This module initializes the Flask application and its core components, such as
SQLAlchemy for database interactions, Bcrypt for password hashing, and Flask-Login
for user session management. It also imports application-specific routes and filters.
"""
from algosdk.v2client.algod import AlgodClient
from flask import Flask  # Core Flask class for creating the application instance
from flask_bcrypt import Bcrypt  # Library for hashing passwords securely
from flask_sqlalchemy import SQLAlchemy  # ORM for database interactions
from flask_login import LoginManager  # Manages user sessions and authentication

from constants import ALGOD_TOKEN, ALGOD_SERVER_ADDRESS

# Create the Flask application instance
app = Flask(__name__)

# Configure application settings
app.config['SECRET_KEY'] = '13ceb0bdfde20b0c64765791628ba245'  # Secret key for session management and CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'  # SQLite database URI

# Initialize SQLAlchemy for database interaction
db = SQLAlchemy(app)

# Initialize Bcrypt for secure password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Login for managing user authentication and sessions
login_manager = LoginManager(app)

algod_client: AlgodClient = AlgodClient(ALGOD_TOKEN, ALGOD_SERVER_ADDRESS)
try:
    status = algod_client.status()
    print("Network Status:", status)
except Exception as e:
    print("Failed to connect:", e)

# Import application routes and filters after initializing the app
from main import routes  # Application's route handlers
from main import filters  # Custom Jinja2 filters
