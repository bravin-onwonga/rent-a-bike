#!/usr/bin/python3
"""Contains the user class"""

from models.base_model import BaseModel, Base
from models.review import Review

from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Class for our users"""

    __tablename__ = 'users'

    firstname = Column(String(128), nullable=False)
    middlename = Column(String(128), nullable=True)
    lastname = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    id_number = Column(String(60), nullable=False)
    phone_number = Column(String(60), nullable=True)
    id_document = Column(String(60), nullable=True)
    profile_pic = Column(String(60), nullable=True)
    password = Column(String(128), nullable=False)
    street_address = Column(String(128), nullable=True)
    county = Column(String(128), nullable=True)
    verified = Column(Boolean, nullable=False, default=False)
    reviews = relationship('Review', backref='user',
                           cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Instantiates a class object"""
        super().__init__(*args, **kwargs)
