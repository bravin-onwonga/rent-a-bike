#!/usr/bin/python3
"""
Setting up flask api using Blueprint
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.views.user import *
from api.views.bike import *
