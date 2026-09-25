
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

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
# tells SQLAlchemy where database lives
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy()
# connects db object(Book class) to Flask web application
db.init_app(app)

# base class that makes this a database table
class Book(db.Model):
    # column uniquely identifying each row
    # necessary fields

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(100))
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400), nullable=False)
    page_count = db.Column(db.Integer, nullable=False)

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
    # __init__() NOT NECESSARY because db.Model has built in constructor
    def __repr__(self):

        return f"Book(isbn={self.isbn}, title={self.title} author={self.author})"

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

@app.route('/new-book')
def add_book():
    book = Book(isbn='9780063462410',
                title="Starlight", 
                author="Alex Aster",
                image='link goes here',
                page_count=500,
                genre='fantasy',
                media_type='digital',
                start_date=datetime.date(2026, 9, 20)
                )
    if book.genre in GENRES and book.media_type in MEDIA_TYPES:
        db.session.add(book)
        db.session.commit()
        return "Book added!"
    else:
        return "Genre or media type invalid!"
    
@app.route('/all-books')
def query_all():
    books = Book.query.all()
    # str(books) internally calls __repr__()
    return str(books)

if __name__ == '__main__':
    with app.app_context():
        # creates database table
        db.create_all()
    app.run(debug=True)
