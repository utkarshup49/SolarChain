from typing import List

from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy import or_

from main import app, bcrypt, db
from main.forms import LoginForm, PurchaseForm, RegistrationForm, SellOrderForm
from main.models import SellOrder, TransactionHistory, User, get_sellers

dashboard_info = {"balance": "50"}

@app.route('/layout')
def layout():
    return render_template("layout.html")


@app.route('/')
@app.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    current = current_user.units
    total = current_user.capacity
    units = units_used(current, total)
    return render_template("index.html", user_data=dashboard_info, units_used=units)


def units_used(current, total):
    proportion = current / total
    return int(proportion * 100)


@app.route('/transactions')
def transactions():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("transaction.html", history=get_transaction_history(current_user.id))


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
        if current_user.units >= units:
            with app.app_context():
                order = SellOrder(user_id=current_user.id, units=units, price=price)
                db.session.add(order)
                db.session.commit()
        else:
            flash('Units not Available!', 'error')

    sell_orders = get_user_sell_orders()
    return render_template("seller_page.html", title="Page", sell_orders=sell_orders, form=form)


@app.route("/buyer_page", methods=['GET', 'POST'])
@login_required
def buyer_page():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    sell_orders = get_sell_orders()
    return render_template("buyer_page.html", title="Buy Units", sell_orders=sell_orders)


@app.route("/cancel_sell_order", methods=["GET", "POST"])
@login_required
def cancel_sell_order():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    order_id = request.args.get("order_id")
    if order_id is None:
        return redirect(url_for("home"))

    with app.app_context():
        order: SellOrder = SellOrder.query.filter_by(id=order_id).first()
        db.session.delete(order)
        db.session.commit()
        flash(f"Order: {order.id} Closed")
    return redirect(url_for('seller_page'))


@app.route("/checkout_page", methods=["GET", "POST"])
@login_required
def checkout_page():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    order_id = request.args.get("order_id")
    if order_id is None:
        return redirect(url_for("home"))

    order: SellOrder = SellOrder.query.filter_by(id=order_id).first()
    seller: User = User.query.filter_by(id=order.user_id).first()
    form = PurchaseForm()
    if form.validate_on_submit():
        if form.units.data <= order.units:
            total_price = order.price * form.units.data
            with app.app_context():
                order: SellOrder = SellOrder.query.filter_by(id=order_id).first()
                buyer: User = User.query.filter_by(id=current_user.id).first()
                seller: User = User.query.filter_by(id=order.user_id).first()
                units = form.units.data
                if seller.units >= units:
                    if buyer.units + form.units.data <= buyer.capacity:
                        buyer.units += units
                        order.units -= units
                        seller.units -= units
                        if order.units == 0:
                            db.session.delete(order)
                        history = TransactionHistory(seller_id=seller.id, seller_username=seller.username, buyer_id=buyer.id, units=units, price=total_price)
                        db.session.add(history)

                        db.session.commit()
                        flash(f"Purchase successful for {form.units.data} units at total {total_price}!")
                        return redirect(url_for('home'))
                    else:
                        flash(f"Purchase unsuccessful for {form.units.data} units. Your Battery is Full!")
                else:
                    flash(f"Purchase unsuccessful for {form.units.data} units. Seller Does Not have these Units!")
        else:
            flash('Units exceeded!', 'error')
    return render_template("checkout_page.html", title="Checkout", order=order, seller=seller, form=form)


def get_user_sell_orders():
    with app.app_context():
        qry = SellOrder.query.filter_by(user_id=current_user.id)
        return qry


def get_transaction_history(user_id):
    with app.app_context():
        history = []
        transacts = TransactionHistory.query.filter(or_(
            TransactionHistory.buyer_id == user_id,
            TransactionHistory.seller_id == user_id
        ))
        for transact in transacts:
            history.append({
                'row': transact,
                'type': "CREDIT" if transact.buyer_id == user_id else "DEBIT"
            })
        return history


def get_sell_orders():
    with app.app_context():
        sell_orders = SellOrder.query.all()  # Assuming you have a SellOrder model
        orders_with_seller = []
        for order in sell_orders:
            seller = User.query.filter_by(id=order.user_id).first()  # Assuming User model has seller info
            if seller.id == current_user.id:
                continue
            orders_with_seller.append({
                'order': order,
                'seller': seller,
                'status': int(order.units > seller.units)
            })
        return orders_with_seller


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("about"))
