#!/usr/bin/python3
"""Contains the lessor class"""

from models.base_model import BaseModel, Base
from models.bike import Bike
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship


class Lessor(BaseModel, Base):
    """Lessor class"""

    __tablename__ = 'lessors'

    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone_number = Column(String(128), nullable=True)
    bike = relationship('Bike', backref='lessor', cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Instantiates a Lessor object"""
        super().__init__(*args, **kwargs)
