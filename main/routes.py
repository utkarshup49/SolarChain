from main.models import User, Sellers, get_sellers
from main.forms import LoginForm, RegistrationForm
from main import app
from flask import Flask, flash, redirect, render_template, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

dashboard_info = {"balance": "50"}

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

