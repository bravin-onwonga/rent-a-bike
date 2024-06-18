#!/usr/bin/python3
"""Contains the lessor class"""

from models.base_model import BaseModel
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship


class Lesser(BaseModel):
    """Lesser class"""

    __tablename__ = 'lessers'

    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone_number = Column(String(128), nullable=True)
    bike = relationship('Bike', backref='lessor', cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Instantiates a Lesser object"""
        super().__init__(*args, **kwargs)
