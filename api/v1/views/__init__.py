#!/usr/bin/python3
"""
Setting up flask api using Blueprint
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.users import *
from api.v1.views.bikes import *
from api.v1.views.lessors import *
from api.v1.views.lessors_bikes import *
from api.v1.views.bikes_reviews import *
