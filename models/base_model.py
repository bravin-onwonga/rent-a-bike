#!/usr/bin/python3
"""Contains the Base Model inherited by other classes"""

from datetime import datetime
from uuid import uuid4 as uid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATE_FMT = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """Base model class"""
    id = Column(String(60), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a Base Model instance"""
        if not kwargs:
            self.id = str(uid())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs.get('updated_at'):
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'],
                    '%Y-%m-%dT%H:%M:%S.%f')
            else:
                setattr(self, 'updated_at', datetime.utcnow())
            if kwargs.get('created_at'):
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'],
                    '%Y-%m-%dT%H:%M:%S.%f')
            else:
                setattr(self, 'created_at', datetime.utcnow())

            if not (kwargs.get('id')):
                kwargs['id'] = str(uid())

            if (kwargs.get('__class__')):
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def save(self):
        """Update the time"""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def __str__(self):
        """Change how __str__ method behaves"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        """Convert to dict"""

        dict_obj = {}

        for obj_key, obj_val in self.__dict__.items():
            if obj_key in {"updated_at", "created_at"}:
                dict_obj[obj_key] = obj_val.isoformat()
            else:
                dict_obj[obj_key] = obj_val

        dict_obj["__class__"] = self.__class__.__name__

        return dict_obj
