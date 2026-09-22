
from flask import Flask

# creates Flask application
# Flask: python framework to create and run website
app = Flask(__name__)

# when client sends request to '/ Flask calls function and sends returns statement back as response
@app.route('/')
def send():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()