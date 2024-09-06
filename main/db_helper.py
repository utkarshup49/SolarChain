from main import app, db
from main.models import User, Sellers

with app.app_context():
    db.create_all()

    # user_1 = User(username="A", password="123")
    # user_2 = User(username="B", password="12")
    #
    # db.session.add(user_1)
    # db.session.add(user_2)
    #
    # user = User.query.first()
    # seller = Sellers(user_id=user.id, location="Test", reputation=4, status=1, price=2.5)
    #
    # db.session.add(seller)
    # db.session.commit()
