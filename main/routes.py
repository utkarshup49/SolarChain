from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, current_user, logout_user

from main import app, bcrypt, db
from main.forms import LoginForm, PurchaseForm, RegistrationForm, SellOrderForm
from main.models import SellOrder, User, get_sellers

dashboard_info = {"balance": "50"}

@app.route('/layout')
def layout():
    return render_template("layout.html")


@app.route('/')
@app.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("index.html", user_data=dashboard_info)


@app.route('/transactions')
def transactions():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("transaction.html", seller_data=get_sellers())


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/account')
def account():
    return render_template("account.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        with app.app_context():
            user = User(username=form.username.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/seller_page", methods=['GET', 'POST'])
@login_required
def seller_page():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    form = SellOrderForm()
    if form.validate_on_submit():
        units, price = form.unit.data, form.price.data
        with app.app_context():
            order = SellOrder(user_id=current_user.id, units=units, price=price)
            db.session.add(order)
            db.session.commit()

    sell_orders = get_user_sell_orders()
    return render_template("seller_page.html", title="Page", sell_orders=sell_orders, form=form)


@app.route("/buyer_page", methods=['GET', 'POST'])
@login_required
def buyer_page():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    form = SellOrderForm()
    if form.validate_on_submit():
        units, price = form.unit.data, form.price.data
        with app.app_context():
            order = SellOrder(user_id=current_user.id, units=units, price=price)
            db.session.add(order)
            db.session.commit()

    sell_orders = get_sell_orders()
    return render_template("buyer_page.html", title="Buy Units", sell_orders=sell_orders, form=form)


@app.route("/checkout_page", methods=["GET", "POST"])
@login_required
def checkout_page():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    order_id = request.args.get("order_id")
    if order_id is None:
        return redirect(url_for("home"))
    order: SellOrder = SellOrder.query.filter_by(id=order_id).first()
    seller = User.query.filter_by(id=order.user_id).first()

    form = PurchaseForm()
    if form.validate_on_submit():
        if form.units.data <= order.units:
            total_price = order.price * form.units.data
            flash(f"Purchase successful for {form.units.data} units at total {total_price}!")
            return redirect(url_for('home'))
        flash('Units exceeded!', 'error')
    return render_template("checkout_page.html", title="Checkout", order=order, seller=seller, form=form)


def get_user_sell_orders():
    with app.app_context():
        qry = SellOrder.query.filter_by(user_id=current_user.id)
        return qry


def get_sell_orders():
    with app.app_context():
        qry = SellOrder.query.filter(SellOrder.user_id != current_user.id).all()
        return qry


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("about"))
