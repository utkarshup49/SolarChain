from main import app, db

# Creates the database file
with app.app_context():
    db.create_all()
