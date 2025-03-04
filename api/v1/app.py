#!/usr/bin/python3
"""Handles api action"""

from api.v1.auth import auth
from flask_session import Session
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from models.user import User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

app.register_blueprint(app_views)
app.register_blueprint(auth)

cors = CORS(app, supports_credentials=True, resources={
    r"/api/v1/*": {"origins": "*"},
    r"/api/v1/auth/*": {"origins": "*"}
})


@app.teardown_appcontext
def close(exception):
    """Calls the close method based on the storage"""
    storage.close()


@app.errorhandler(404)
def handle_404_error(ex):
    """Handles the page not found(404) error"""
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
