#!/usr/bin/python3
"""Contains the bike class"""


from datetime import datetime
from models.base_model import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime

class Bike(BaseModel):
    """Bikes class

    Attributes:
        model
    """
    __tablename__ = 'bikes'

    model = Column(String(60), nullable=False)
    type = Column(String(128), nullable=False)
    available = Column(Boolean, default=True)
    lessor_id = Column(String(60), ForeignKey('lessor.id'), nullable=False)
    user_id = Column(String(60), nullable=False)
    rent_date = Column(DateTime, nullable=True)
    return_date = Column(DateTime, nullable=True)

    def __init__(self, *args, **kwargs):
        """Instantiates our object"""
        super().__init__(*args, **kwargs)

    def rent(self, **kwargs):
        """Method to allow a user to rent a bike"""
        for key, value in kwargs.items():
            setattr(key, value)
        self.updated_at = datetime.utcnow()
