#!/usr/bin/python3
"""Contains the admin class"""

from models.base_model import BaseModel


class Admin(BaseModel):
    """Admin class

    Attributes:
        name - name of the admin
        email - admins email
        password - admins password
    """
    name = ""
    email = ""
    password = ""

    def __init__(self, *args, **kwargs):
        """Instantiates our object"""
        super().__init__(*args, **kwargs)
