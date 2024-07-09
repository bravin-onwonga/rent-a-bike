#!/usr/bin/python3
"""
Handles the api calls for the relationship between
the lessors and bikes
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.bike import Bike
from models.review import Review
from models.user import User


@app_views.route('/bikes/<bike_id>/reviews', methods=['GET'])
def get_bike_reviews(bike_id):
    """Get a bikes reviews"""
    bike = storage.get(Bike, bike_id)

    if bike:
        bike_lst = []
        reviews = storage.all(Review)

        for review in reviews.values():
            review_dict = review.to_dict()
            if review_dict.get('bike_id') == bike_id:
                bike_lst.append(review_dict)

        return jsonify(bike_lst), 200
    else:
        abort(400)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Gets a Review using its id"""
    review = storage.get(Review, review_id)

    if review:
        return jsonify(review.to_dict()), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """Deletes a review based on the ID passed"""
    review = storage.get(Review, review_id)

    if review:
        storage.delete(review)
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/bikes/<bike_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def post_review(bike_id):
    """Makes a post request"""
    if not request.is_json:
        return (jsonify('Not a JSON'), 400)
    bike = storage.get(bike, bike_id)
    if not bike:
        abort(404)
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return (jsonify('Missing user_id'), 400)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    obj = Review(**data)
    storage.new(obj)
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def alter_review(review_id):
    """alters a review based on the ID passed"""
    data = request.get_json()

    if not data:
        return jsonify({'Not a JSON'}), 400

    obj = storage.get(Review, review_id)

    if obj:
        lst = ['id', 'user_id', 'bike_id', 'created_at', 'updated_at']
        for key in lst:
            if data.get(key):
                del data[key]
        for key, value in data.items():
            setattr(obj, key, value)
        storage.save()
        return (jsonify(obj.to_dict()), 200)
    else:
        abort(404)
