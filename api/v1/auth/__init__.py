#!/usr/bin/python3
"""
Setting up flask api using Blueprint
"""

from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

from api.v1.auth.auth import *
