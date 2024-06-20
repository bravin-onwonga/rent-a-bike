#!/usr/bin/python3
"""Contains the Review Class"""

from models.base_model import BaseModel, Base

from sqlalchemy import ForeignKey, Column, String, DateTime
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """Review for each object"""
    __tablename__ = 'reviews'

    bike_id = Column(String(60), ForeignKey('bikes.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a review obj inheriting from the BaseModel class"""
        super().__init__(*args, **kwargs)
