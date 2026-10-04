
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY')

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
    cover = db.Column(db.String(400), nullable=False)
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

# take what GoogleBooks API gives me, reshape and send back to json
@app.route('/search-books')
def search():
    # gets the user's search which is the query
    query = request.args.get('q')
    # calls external API and retrieves search results
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}')
    # gets the response and converts to json
    data = response.json()
    # converts python dict/list into JSON HTTP response
    results = []
    # item represents each search result
    for item in data['items']:
        # volumeInfo is the key where the actual info we care about from each search result
        volInfo = item['volumeInfo']
        saleInfo = item.get('saleInfo', {})
        isbn = None
        for identifier in volInfo.get('industryIdentifiers', {}):
            if identifier.get('type') == 'ISBN_13':
                isbn = identifier.get('identifier')

        results.append({
            # get just isbn 13
            'isbn': isbn,
            'title': volInfo.get("title"),
            'author': volInfo.get("authors"),
            'cover': volInfo.get('imageLinks', {}).get('thumbnail', ''),
            'page_count': volInfo.get('pageCount'),
            'type': saleInfo.get('isEbook')
        })

    return jsonify(results)

@app.route('/render-books')
def render_templates():
    return render_template('search.html')

@app.route('/new-book')
def add_book():
    book = Book(isbn='9780063462410',
                title="Starside", 
                author="Alex Aster",
                cover='link goes here',
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
