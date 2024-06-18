#!/usr/bin/python3
"""Contains the bike class"""


from models.base_model import BaseModel

class Bike(BaseModel):
    """Bikes class

    Attributes:
        model
    """

    model = ""
    lessor_id = ""
    available = ""
    user_id = ""

    def __init__(self, *args, **kwargs):
        """Instantiates our object"""
        super().__init__(*args, **kwargs)
