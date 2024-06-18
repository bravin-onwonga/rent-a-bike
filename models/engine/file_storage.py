#!/usr/bin/python3
"""First storage is the file storage"""

from models.user import User
from models.admin import Admin
from models.lessor import Lessor
from models.bike import Bike


classes = {"User": User, "Lessor": Lessor, "Admin": Admin, "Bike": Bike}

class FileStorage:
    """File storage logic"""
    __object = {}
    __filepath = "file.json"

    def __init__(self):
        """Instantiates my file storage"""
