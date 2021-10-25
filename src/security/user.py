from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_, name, password, roles,rid):
        self.id = id_
        self.rid = rid
        self.name = name
        self.password = password
        self.roles = roles

    def has_role(self, role):
        return role in self.roles