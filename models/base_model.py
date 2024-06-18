#!/usr/bin/python3
"""Contains the Base Model inherited by other classes"""

from datetime import datetime
from uuid import uuid4 as uid
from models import storage
from sqlalchemy import Column, String, DateTime

DATE_FMT = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """Base model class"""
    def __init__(self, *args, **kwargs):
        """Instantiates a Base Model instance"""

        id = Column(String(60), primary_key=True, unique=True, nullable=False)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

        def __init__(self, *args, **kwargs):
            if not kwargs:
                self.id = str(uid)
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            else:
                for key, val in kwargs.items():
                    if key in {"created_at", "updated_at"}:
                        setattr(
                            self, key, datetime.strptime(val, BaseModel.DATE_FMT)
                        )
                    elif key != "__class__":
                        setattr(self, key, val)

    def save(self):
        """Update the time"""

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