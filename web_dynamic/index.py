#!/usr/bin/python3
""" Starts a Flash Web Application """
import uuid
from models import storage
from flask import Flask, render_template

from models.bike import Bike
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

@app.route('/home', strict_slashes=False)
def home():
    """ Home(Landing) Page"""
    bikes = storage.all(Bike).values()

    return render_template('home.html', bikes=bikes, cache_id=uuid.uuid4())

@app.route('/bikes', strict_slashes=False)
def bikes():
    """ Bikes page"""
    bikes = storage.all(Bike).values()

    return render_template('bikes.html', bikes=bikes, cache_id=uuid.uuid4())


@app.route('/services', strict_slashes=False)
def services():
    """ Services """

    return render_template('services.html', bikes=bikes, cache_id=uuid.uuid4())

@app.route('/lessors', strict_slashes=False)
def lessors():
    """ Services """

    return render_template('lessors.html', bikes=bikes, cache_id=uuid.uuid4())

@app.route('/contact', strict_slashes=False)
def contact():
    """ Contact """

    return render_template('contact.html', bikes=bikes, cache_id=uuid.uuid4())

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001, debug=True)