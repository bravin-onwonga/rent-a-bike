#!/usr/bin/python3
"""Contains the user class"""

from models.base_model import BaseModel

from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship

class User(BaseModel):
    """Class for our users"""

    __tablename__ = 'users'

    firstname = Column(String(128), nullable=False)
    middlename = Column(String(128), nullable=True)
    lastname = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    id_number = Column(String(60), nullable=False)
    phone_number = Column(String(60), nullable=True)
    profile_pic = Column(String(60), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    password = Column(String(128), nullable=False)
    street_address = Column(String(128), nullable=True)
    county = Column(String(128), nullable=True)
    bikes_rented = []
    reviews = []

    def __init__(self, *args, **kwargs):
        """Instantiates a class object"""
        super().__init__(*args, **kwargs)
