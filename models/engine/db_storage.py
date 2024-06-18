#!/usr/bin/python3
"""Contains the database storage logic"""

import os
from sqlalchemy import MetaData, create_engine
from models.user import User
from models.admin import Admin
from models.lessor import Lesser
from models.bike import Bike

cls_lst = [User, Admin, Lesser, Bike]

class DBStorage:
    """My database storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates the class object"""
        username = ""
        dbname = ""
        host = ""
        passwd = ""

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                username,
                passwd,
                host,
                dbname),
                pool_pre_ping=True)

        def all(self, cls):
            """Lists all object of a class or
            all object if no class is given"""

            my_dict = {}
            if (cls):
                objs = self.__session.query(cls).all()

                for obj in objs:
                    key = cls.__name__ + "+" + obj.id
                    value = obj
                    my_dict.update({key: value})
            else:
                for cls in cls_list:
                    objs = self.__session.query(cls).all()

                    for obj in objs:
                        key = cls.__name__ + "+" + obj.id
                        value = obj
                        my_dict.update({key: value})

            return my_dict


        def new(self, obj=None):
            if obj:
                self.__session.add(obj)


        def save(self):
            self.__session.commit()

        def delete(self, obj=None):
            if obj:
                obj_cls = obj.__class__
                key = obj_cls + "." + obj.id
                obj_to_del = self.__session.query(obj_cls).filter(obj_cls.id == key)

                if obj_to_del:
                    self.__session.delete(obj_to_del)

        def close(self):
            self.__session.close()
            self.reload()
