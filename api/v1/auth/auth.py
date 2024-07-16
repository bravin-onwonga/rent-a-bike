from flask import abort, request, redirect, session, url_for, jsonify
from models import storage
from models.user import User
import hashlib
from api.v1.auth import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Logs in the user"""
    if request.method == 'POST':
        login_data = request.get_json()
        if not login_data:
            abort(400, 'Missing information')
        email = login_data.get('email')
        password = login_data.get('password')
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        user = storage.get_user_by_email(email)
        if user and user.to_dict().get('password') == hashed_password:
            session['user_id'] = user.id
            return jsonify(user.to_dict()), 200
        else:
            abort(404)


@auth.route('/logout', strict_slashes=False)
def logout():
    """Logout a login user"""
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200


@auth.route('/current_user', methods=['GET'])
def get_current_user():
    """Gets the current user if logged in"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    user = storage.get(User, user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404
