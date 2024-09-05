import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


# Connect to the SQLite database
def get_sellers():
    connection = sqlite3.connect('sellers.db')  # Your SQLite database file
    cursor = connection.cursor()

    # Fetch data from the sellers table
    cursor.execute("SELECT name, location, reputation, available, price_per_kwh FROM sellers")
    sellers = cursor.fetchall()

    connection.close()
    return sellers


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/transactions')
def transactions():
    return render_template("transaction.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
