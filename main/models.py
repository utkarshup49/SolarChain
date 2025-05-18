"""
This module defines database models, user authentication, and utility functions for the application.
It provides structure for storing and managing user-related data, transactions, and other application-specific records.
"""


import random  # Used for generating default values for certain fields
from main import db, login_manager  # Database instance and login manager from the main app
from flask_login.mixins import UserMixin  # Mixin for handling user session functionality


# Function to load a user by their ID for session management
@login_manager.user_loader
def load_user(user_id):
    """
    Callback function for Flask-Login to load a user by their ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The User object corresponding to the given ID, or None if not found.
    """
    return User.query.get(int(user_id))


# Database model representing a user in the system
class User(db.Model, UserMixin):
    """
    Represents a user in the database.

    Attributes:
        id (int): Primary key for the user.
        username (str): Unique username for the user.
        image_file (str): Path to the user's profile image.
        password (str): Hashed password for the user.
        units (int): Available units the user owns (default is a random value between 1 and 10).
        seller_rep (int): Seller reputation score (default is a random value between 1 and 5).
        sell_orders (list): Relationship to the user's sell orders.

    Methods:
        __repr__(): Provides a string representation of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="profile.jpg")
    password = db.Column(db.String(60), unique=True, nullable=False)
    units = db.Column(db.Integer, default=random.randint(1, 10))
    seller_rep = db.Column(db.Integer, default=random.randint(1, 5))
    sell_orders = db.relationship("SellOrder", backref="seller", lazy=False)
    wallet_public_key = db.Column(db.String(100), nullable=True)

    def __repr__(self) -> str:
        return f"{self.id} {self.username} {self.password} {self.image_file}"


# Database model representing a sell order
class SellOrder(db.Model):
    """
    Represents a sell order in the database.

    Attributes:
        id (int): Primary key for the sell order.
        user_id (str): Foreign key linking to the seller's user ID.
        units (int): Number of units in the sell order.
        price (float): Price per unit in the sell order.
        status (int): Status of the order (default is 0).
        buyer_id (str): ID of the buyer (if applicable).

    Methods:
        __repr__(): Provides a string representation of the sell order.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey("user.id"), nullable=False)
    units = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Double, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    buyer_id = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.units} {self.price}"


# Database model representing transaction history
class TransactionHistory(db.Model):
    """
    Represents a transaction history record in the database.

    Attributes:
        id (int): Primary key for the transaction.
        seller_id (int): Foreign key linking to the seller's user ID.
        seller_username (str): Username of the seller.
        buyer_id (int): Foreign key linking to the buyer's user ID.
        units (int): Number of units in the transaction.
        price (float): Price of the transaction.
        date (datetime): Date and time of the transaction.
    """
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seller_username = db.Column(db.String(50), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    units = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Double, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


# Utility function to retrieve all sellers from the database
def get_sellers():
    """
    Queries all sell orders from the database.

    Returns:
        list: A list of SellOrder objects representing all sell orders in the system.
    """
    return SellOrder.query.all()
