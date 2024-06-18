#!/usr/bin/python3
"""Contains the bike class"""


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
    rent_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates our object"""
        super().__init__(*args, **kwargs)
