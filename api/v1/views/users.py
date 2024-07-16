#!/usr/bin/python3
"""
Module to handle restful api actions for the user
"""

from flask import abort, flash, jsonify, redirect, request, url_for
from api.v1.views import app_views
from models import storage
from models.bike import Bike
from models.user import User
import hashlib


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Gets all users from DB"""
    users_lst = []
    users = storage.all(User)

    for user in users.values():
        users_lst.append(user)
    return jsonify(users_lst), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Gets one user using the user's id"""
    user = storage.get(User, user_id)

    if user:
        return jsonify(user), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>/bikes',
                 strict_slashes=False,
                 methods=['GET'])
def get_user_bikes(user_id):
    """Gets one bike instance by its id"""
    bikes_lst = []

    bikes = storage.all(Bike)

    for bike in bikes.values():
        if bike.get(user_id) == user_id:
            bikes_lst.append(bike)
    return jsonify(bikes_lst), 200


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User based on the ID passed"""
    user = storage.get(User, user_id)

    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    user_info = request.get_json()

    errors = ['email',
              'firstname',
              'lastname',
              'id_number']

    if not user_info:
        abort(400, 'Missing information')
    for key in errors:
        if not (user_info.get(key)):
            if (key == "phone_number"):
                abort(400, "Missing phone number")
            abort(400, "Missing {}".format(key))

    passwd = user_info['password']

    hashed_password = hashlib.md5(passwd.encode('utf-8')).hexdigest()

    user = {
        "firstname": user_info['firstname'],
        "middlename": user_info.get('middlename', ''),
        "lastname": user_info['lastname'],
        "email": user_info['email'],
        "id_number": user_info['id_number'],
        "phone_number": user_info.get('phone_number', ''),
        "password": hashed_password,
        "county": user_info.get('county', ''),
        "street_address": user_info.get('street_address', '')
    }

    new_user = User(**user)
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Updates the user data using his id"""
    new_info = request.get_json()

    if not new_info.get('firstname') or not new_info.get('lastname'):
        abort(400, "Missing firstname or lastname")

    if not new_info:
        abort(400, "Missing information")

    user = storage.get(User, user_id)

    if user:
        lst = ['id', 'updated_at', 'created_at']
        for key in lst:
            if new_info.get(key):
                del new_info[key]
        for key, value in new_info.items():
            setattr(user, key, value)
        storage.save()
        return jsonify(user), 200
    else:
        abort(404)
