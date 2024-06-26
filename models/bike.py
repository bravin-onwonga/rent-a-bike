#!/usr/bin/python3
"""Contains the bike class"""

from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from models.review import Review


class Bike(BaseModel, Base):
    """Bikes class

    Attributes:
        model
    """
    __tablename__ = 'bikes'

    model = Column(String(60), nullable=False)
    category = Column(String(128), nullable=False)
    price = Column(String(30), nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    user_id = Column(String(60), nullable=True)
    rent_date = Column(DateTime, nullable=True)
    return_date = Column(DateTime, nullable=True)
    lessor_id = Column(String(60), ForeignKey('lessors.id'), nullable=False)
    reviews = relationship('Review', backref='bike')

    def __init__(self, *args, **kwargs):
        """Instantiates our object"""
        super().__init__(*args, **kwargs)

    def rent_bike(self, **kwargs):
        """Method to allow a user to rent a bike"""
        for key, value in kwargs.items():
            setattr(key, value)
        self.updated_at = datetime.utcnow()
