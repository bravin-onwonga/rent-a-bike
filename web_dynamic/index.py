#!/usr/bin/python3
""" Starts a Flash Web Application """
import uuid
from models import storage
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/login', strict_slashes=False)
def login():
    """ HBNB is alive! """

    return render_template('login.html', cache_id=uuid.uuid4())

@app.route('/signup', strict_slashes=False)
def signup():
    """ HBNB is alive! """

    return render_template('signup.html', cache_id=uuid.uuid4())


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)