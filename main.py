import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


dashboard_info = {"balance": "50"}


# Connect to the SQLite database
def get_sellers():
    connection = sqlite3.connect('sellers.db')  # Your SQLite database file
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS sellers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        location TEXT,
                        reputation REAL,
                        available INTEGER,
                        price_per_kwh REAL
                      )''')

    # Fetch data from the sellers table
    cursor.execute("SELECT name, location, reputation, available, price_per_kwh FROM sellers")
    sellers = cursor.fetchall()
    print(sellers)

    connection.close()
    return sellers


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", user_data=dashboard_info)


@app.route('/transactions')
def transactions():
    return render_template("transaction.html", seller_data=get_sellers())


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/layout')
def layout():
    return render_template("layout.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
