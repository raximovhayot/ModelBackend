from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    print("Flask and Werkzeug are compatible!")
    with app.test_request_context():
        print("URL for index:", url_for('index'))
