import random

from main import db, login_manager
from flask_login.mixins import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="profile.jpg")
    password = db.Column(db.String(60), unique=True, nullable=False)
    units = db.Column(db.Integer, default=random.randint(1, 10))
    capacity = db.Column(db.Integer, default=random.randint(10, 100))
    seller_rep = db.Column(db.Integer, default=random.randint(1, 5))
    sell_orders = db.relationship("SellOrder", backref="seller", lazy=False)

    def __repr__(self) -> str:
        return f"{self.id} {self.username} {self.password} {self.image_file}"


class SellOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey("user.id"), nullable=False)
    units = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Double, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    buyer_id = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f"{self.id} {self.user_id} {self.units} {self.price}"


class Sellers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    reputation = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0)


class TransactionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)



# Connect to the SQLite database
def get_sellers():
    # connection = sqlite3.connect('sellers.db')  # Your SQLite database file
    # cursor = connection.cursor()
    #
    # cursor.execute('''CREATE TABLE IF NOT EXISTS sellers (
    #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     name TEXT NOT NULL,
    #                     location TEXT,
    #                     reputation REAL,
    #                     available INTEGER,
    #                     price_per_kwh REAL
    #                   )''')
    #
    # # Fetch data from the sellers table
    # cursor.execute("SELECT name, location, reputation, available, price_per_kwh FROM sellers")
    # sellers = cursor.fetchall()
    #
    # connection.close()
    return SellOrder.query.all()
