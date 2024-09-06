import sqlite3

from flask import Flask, flash, redirect, render_template, url_for

from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '13ceb0bdfde20b0c64765791628ba245'
# db = SQLAlchemy(app)
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


@app.route('/layout')
def layout():
    return render_template("layout.html")


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


@app.route('/account')
def account():
    return render_template("account.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'test' and form.password.data == '123':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
