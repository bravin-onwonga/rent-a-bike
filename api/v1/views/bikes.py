#!/usr/bin/python3
"""Handles bike class API requests"""

from datetime import datetime
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
        bikes_lst.append(bike)

    return jsonify(bikes_lst), 200


@app_views.route('/bikes/available', strict_slashes=False, methods=['GET'])
def get_available_bikes():
    """Get available bikes"""
    bikes_lst = []

    bikes = storage.all(Bike)

    for bike in bikes.values():
        if bike.available:
            bikes_lst.append(bike)

    return jsonify(bikes_lst), 200


@app_views.route('/bikes/<bike_id>', strict_slashes=False, methods=['GET'])
def get_bike(bike_id):
    """Gets one bike instance by its id"""
    bike = storage.get(Bike, bike_id)

    if bike:
        return jsonify(bike), 200
    else:
        abort(400, "Bike not found")


@app_views.route('/bikes/<bike_id>', strict_slashes=False, methods=['DELETE'])
def delete_bike(bike_id):
    """Deletes a bike using its id"""
    bike = storage.get(Bike, bike_id)

    if bike:
        storage.delete(bike)
        storage.save()
        return jsonify({}), 202
    else:
        abort(404)


@app_views.route('/bikes', strict_slashes=False, methods=['POST'])
def create_Bike():
    bike_info = request.get_json()

    errors = ["model", "category", "lessor_id"]

    if not bike_info:
        abort(400, 'Missing information')
    for key in errors:
        if not (bike_info.get(key)):
            abort(400, "Missing {}".format(key))
    new_bike = Bike(**bike_info)
    storage.new(new_bike)
    storage.save()
    return jsonify(new_bike.to_dict()), 201


@app_views.route('/bikes/<bike_id>', strict_slashes=False, methods=['PUT'])
def update_bike(bike_id):
    """Updates the Bike data using his id"""
    new_info = request.get_json()

    if not (new_info):
        abort(400, "Missing information")

    new_info['rent_date'] = datetime.utcnow()

    bike = storage.get_instance(Bike, bike_id)

    print(bike)

    if bike:
        lst = ['id', 'updated_at', 'created_at']

        for key, value in new_info.items():
            if key not in lst:
                setattr(bike, key, value)
        storage.save()
        return jsonify(bike.to_dict()), 200
    else:
        abort(404)
