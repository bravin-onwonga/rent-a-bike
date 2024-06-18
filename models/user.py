#!/usr/bin/python3
"""Contains the user class"""

from models.base_model import BaseModel

class User(BaseModel):
    """Class for our lessee"""

    firstname = ""
    lastname = ""
    email = ""
    id_number = ""
    phone_number = ""
    profile_pic = ""
    date_of_birth = ""
    password = ""
    street_address = ""
    zip_code = ""
    county = ""
    bikes_rented = []
    reviews = []

    def __init__(self, *args, **kwargs):
        """Instantiates a class object"""
        super().__init__(*args, **kwargs)
