#!/usr/bin/python3
"""Handles Lessor class API requests"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.lessor import Lessor


@app_views.route('/lessors', strict_slashes=False, methods=['GET'])
def get_lessors():
    """Get all Lessors"""
    lessors_lst = []

    lessors = storage.all(Lessor)

    for lessor in lessors.values():
        lessors_lst.append(lessor)

    return jsonify(lessors_lst), 200


@app_views.route('/lessors/<lessor_id>', strict_slashes=False, methods=['GET'])
def get_Lessor(lessor_id):
    """Gets one Lessor instance by its id"""
    lessor = storage.get(Lessor, lessor_id)

    if lessor:
        return jsonify(lessor), 200
    else:
        abort(400, "Lessor not found")


@app_views.route('/lessors', strict_slashes=False, methods=['POST'])
def create_lessor():
    lessor_info = request.get_json()

    errors = ["model", "category", "lessor_id"]

    if not lessor_info:
        abort(400, 'Missing information')
    for key in errors:
        if not (lessor_info.get(key)):
            abort(400, "Missing {}".format(key))
    new_lessor = Lessor(**lessor_info)
    storage.new(new_lessor)
    storage.save()
    return jsonify(new_lessor.to_dict()), 201


@app_views.route('/lessors/<lessor_id>', strict_slashes=False, methods=['PUT'])
def update_lessor(lessor_id):
    """Updates the Lessor data using his id"""
    new_info = request.get_json()

    if not new_info:
        abort(400, "Not a JSON")

    if not new_info.get('firstname') or not new_info.get('lastname'):
        abort(400, "Missing firstname or lastname")

    Lessor = storage.get(Lessor, lessor_id)

    if Lessor:
        lst = ['id', 'updated_at', 'created_at']
        for key in lst:
            if new_info.get(key):
                del new_info[key]
        for key, value in new_info.items():
            setattr(Lessor, key, value)
        storage.save()
        return jsonify(Lessor), 200
    else:
        abort(404)
