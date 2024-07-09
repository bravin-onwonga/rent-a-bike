#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import Flask, render_template
from models.bike import Bike
from models.lessor import Lessor
from models import storage
import uuid

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


@app.route('/', strict_slashes=False)
def default():
    """ Landing url """

    return render_template('home.html', cache_id=uuid.uuid4())


@app.route('/home', strict_slashes=False)
def home():
    """ Home(Landing) Page"""
    bikes = storage.all(Bike).values()
    mountain_bikes = []
    road_bikes = []
    adventure_bikes = []

    for bike in bikes:
        if bike.get('category') == 'mountain':
            mountain_bikes.append(bike)
        elif bike.get('category') == 'road':
            road_bikes.append(bike)
        elif bike.get('category') == 'adventure':
            adventure_bikes.append(bike)

    return render_template('home.html',
                           mountain_bikes=mountain_bikes,
                           road_bikes=road_bikes,
                           adventure_bikes=adventure_bikes,
                           cache_id=uuid.uuid4())


@app.route('/bikes', strict_slashes=False)
def bikes():
    """ Bikes page"""
    bikes = storage.all(Bike).values()
    available_bikes = [bike for bike in bikes if bike.get('available')]

    for bike in available_bikes:
        if bike in bikes:
            print(bike)

    return render_template('bikes.html',
                           bikes=available_bikes,
                           cache_id=uuid.uuid4())


@app.route('/about', strict_slashes=False)
def about():
    """ About """

    return render_template('about.html', bikes=bikes, cache_id=uuid.uuid4())


@app.route('/lessors', strict_slashes=False)
def lessors():
    """ Lessors """
    lessors = storage.all(Lessor).values()

    return render_template('lessors.html',
                           lessors=lessors,
                           cache_id=uuid.uuid4())


@app.route('/contact', strict_slashes=False)
def contact():
    """ Contact """

    return render_template('contact.html', bikes=bikes, cache_id=uuid.uuid4())


@app.route('/bike/<model>', strict_slashes=False)
def product(model):
    """ View product """
    bike = None

    bikes = storage.all(Bike).values()

    for b in bikes:
        if b.get('model') == model:
            bike = b
            break

    lessor = None

    if bike:
        lessor = storage.get(Lessor, bike.get('lessor_id'))

    return render_template('display.html',
                           bike=bike,
                           lessor=lessor,
                           cache_id=uuid.uuid4())


@app.route('/bike/mountain', strict_slashes=False)
def display_mountain():
    """ Display mountain bikes """
    bikes = storage.all(Bike).values()
    mountain_bikes = []

    for bike in bikes:
        if bike.get('category') == 'mountain':
            mountain_bikes.append(bike)

    return render_template('mountain.html',
                           mountain_bikes=mountain_bikes,
                           cache_id=uuid.uuid4())


@app.route('/bike/road', strict_slashes=False)
def display_road():
    """ Display road bikes """
    bikes = storage.all(Bike).values()
    road_bikes = []

    for bike in bikes:
        if bike.get('category') == 'mountain':
            road_bikes.append(bike)

    return render_template('road.html',
                           road_bikes=road_bikes,
                           cache_id=uuid.uuid4())


@app.route('/bike/adventure', strict_slashes=False)
def display_adventure():
    """ Display adventure bikes """
    bikes = storage.all(Bike).values()
    adventure_bikes = []

    for bike in bikes:
        if bike.get('category') == 'mountain':
            adventure_bikes.append(bike)

    return render_template('adventure.html',
                           adventure_bikes=adventure_bikes,
                           cache_id=uuid.uuid4())


@app.route('/cart', strict_slashes=False)
def cart():
    """Link to cart template"""
    return render_template('cart.html', cache_id=uuid.uuid4())


@app.route('/checkout', strict_slashes=False)
def checkout():
    """Checkout page"""
    return render_template('checkout.html', cache_id=uuid.uuid4())


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001, debug=True)
