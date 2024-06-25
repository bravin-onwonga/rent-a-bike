#!/usr/bin/python3
"""Handles bike class API requests"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.bike import Bike

@app_views.route('/bikes', strict_slashes=False, methods=['GET'])
def get_bikes():
    """Get all bikes"""
    bikes_lst = []

    bikes = storage.all(Bike)

    for bike in bikes.values():
        bikes_lst.append(bike.to_dict())

    return jsonify(bikes_lst), 200

@app_views.route('/bikes/<bike_id>', strict_slashes=False, methods=['GET'])
def get_bike(bike_id):
    """Gets one bike instance by its id"""
    bike = storage.get(Bike, bike_id)

    if bike:
        return jsonify(bike.to_dict()), 200
    else:
        abort(400, "Bike not found")


@app_views.route('/bikes', strict_slashes=False, method=['POST'])
def create_Bike():
    bike_info = request.get_json()

    errors = ["model", "category", "lessor_id"]

    if not bike_info:
        abort(400, 'Missing information')
    for key in errors:
        if not(bike_info.get(key)):
            abort(400, "Missing {}".format(key))
    new_bike = Bike(**bike_info)
    storage.new(new_bike)
    storage.save()
    return jsonify(new_bike.to_dict()), 201

@app_views.route('/bikes/<bike_id>', strict_slashes=False, methods=['PUT'])
def update_bike(bike_id):
    """Updates the Bike data using his id"""
    new_info = request.get_json()

    if not new_info.get('firstname') or not new_info.get('lastname'):
        abort(400, "Missing firstname or lastname")

    if not(new_info):
        abort(400, "Missing information")

    bike = storage.get(Bike, bike_id)

    if bike:
        lst = ['id', 'updated_at', 'created_at']
        for key in lst:
            if new_info.get(key):
                del new_info[key]
        for key, value in new_info.items():
            setattr(bike, key, value)
        storage.save()
        return jsonify(bike.to_dict()), 200
    else:
        abort(404)
