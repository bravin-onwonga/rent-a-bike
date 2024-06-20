#!/usr/bin/python3
"""My console environment"""

import cmd
from datetime import datetime


class HBNBCommand(cmd.Cmd):
    """Class inheriting from the cmd.Cmd"""
    prompt = "r.a.b& "

    def do_EOF(self, line):
        """Ctrl-D to exit the program"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        from models.user import User
        from models.lessor import Lessor
        from models.admin import Admin
        from models.bike import Bike
        from models import storage

        classes = {"User": User, "Lessor": Lessor,
                   "Admin": Admin, "Bike": Bike}

        args_lst = args.split(" ")
        class_name = args_lst[0]

        if not class_name:
            print("** class name missing **")
            return

        if class_name not in classes:
            print("** class doesn't exist **")
            return

        new_instance = classes[class_name]()

        for item in args_lst[1:]:
            if '=' in item:
                key, value = item.split('=', 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value.strip('"').replace('_', ' ')
                elif '.' in value:
                    value = float(value)
                elif key == "date_of_birth":
                    date_of_birth = datetime.strptime(value, "%Y-%m-%d").date()
                else:
                    value = int(value)

                setattr(new_instance, key, value)

        storage.new(new_instance)
        print(new_instance.id)
        storage.save()

    @staticmethod
    def _split(line):
        """splits my line using spaces
        Return a dict"""
        import shlex

        return shlex.split(line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
