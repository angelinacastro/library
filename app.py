
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

GENRES = [
        "fiction", 
        "romance", 
        "fantasy", 
        "horror", 
        "mystery",
        "non-fiction"
          ]

MEDIA_TYPES = [
        "digital", 
        "physical"
        ]

# creates Flask application
# Flask: python framework to create and run website
app = Flask(__name__)

db = SQLAlchemy()

# base class that makes this a database table
class Book(db.Model):
    # column uniquely identifying each row
    # necessary fields

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(100))
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)

    # chosen from categories
    genre = db.Column(db.String(100), nullable=False)
    media_type = db.Column(db.String(100), nullable=False)

    # optional fields
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    rating = db.Column(db.Integer)
    __table_args__ = (
        db.CheckConstraint('rating <= 5 AND rating >= 0'),
    )

"""
if genre not in GENRES:
    don't add book object
"""

# when client sends request to '/ Flask calls function and sends returns statement back as response
@app.route('/')
def send():
    return 'Hello World!'

@app.route('/about')
def about_page():
    return 'This is the about page!'

if __name__ == '__main__':
    app.run(debug=True)
