#!/usr/bin/python3
"""
Handles the api calls for the relationship between
the lessors and bikes
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.bike import Bike
from models.lessor import Lessor


@app_views.route('/lessors/<lessor_id>/bikes',
                 strict_slashes=False, methods=['GET'])
def all_lessor_bikes(lessor_id):
    """Gets all bikes lessed by a lessor"""
    lessor = storage.get(Lessor, lessor_id)

    if lessor:
        bikes_lst = []
        bikes = storage.all(Bike)

        for bike in bikes.values():
            bike_dict = bike
            if bike_dict.get('lessor_id') == lessor_id:
                bikes_lst.append(bike_dict)

        return jsonify(bikes_lst), 200
    else:
        abort(404)
