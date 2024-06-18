#!/usr/bin/python3
"""Contains the Base Model inherited by other classes"""

from datetime import datetime
from uuid import uuid4 as uid

class BaseModel:
    """Base model class"""
    def __init__(self, *args, **kwargs):
        """Instantiates a Base Model instance"""
        id = str(uid)
        created_at = datetime.now()
        updated_at = created_at()
