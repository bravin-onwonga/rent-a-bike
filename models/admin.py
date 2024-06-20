#!/usr/bin/python3
"""Contains the admin class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Boolean, Column, String, DateTime


class Admin(BaseModel, Base):
    """Admin class

    Attributes:
        name - name of the admin
        email - admins email
        password - admins password
    """
    __tablename__ = 'admin'

    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates our object"""
        super().__init__(*args, **kwargs)
