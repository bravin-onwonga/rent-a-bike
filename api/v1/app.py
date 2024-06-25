#!/usr/bin/python3
"""Handles api action"""

from flask import Flask, jsonify
from models.storage import storage

app = Flask(__name__)

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
