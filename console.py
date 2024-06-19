#!/usr/bin/python3
"""My console environment"""

import cmd

class HBNBCommand(cmd.Cmd):
    """Class inheriting from the cmd.Cmd"""
    prompt = "r.a.b&"

    def do_EOF(self, line):
        """Ctrl-D to exit the program"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        pass

    def do_create(self, line):
        """Creates a new object"""
        my_lst = self._split(line)

        from models.user import User
        from models.lessor import Lessor
        from models.admin import Admin
        from models.bike import Bike

        classes = {"User": User, "Lessor": Lessor, "Admin": Admin, "Bike": Bike}


    @staticmethod
    def _split(line):
        """splits my line using spaces
        Return a dict"""
        import shlex

        return shlex.split(line)
