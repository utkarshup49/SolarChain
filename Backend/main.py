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
def show_table():
    # Fetch the seller data
    # sellers = get_sellers()

    # Pass the data to the HTML template to render
    return "Test"


# if __name__ == '__main__':
#     app.run(debug=True)
