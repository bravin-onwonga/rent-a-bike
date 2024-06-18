#!/usr/bin/python3
"""Contains the lessor class"""

from models.base_model import BaseModel


class Lesser(BaseModel):
    """Lesser class"""
    name = ""
    email = ""
    phone_number = ""
    facebook_profile = ""
    instagram_profile = ""
    twitter_profile = ""
    bikes = []

    def __init__(self, *args, **kwargs):
        """Instantiates a Lesser object"""
        super().__init__(*args, **kwargs)
