from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, dpi, contrasena, cargo="", nombre="") -> None:
        self.id = id
        self.dpi = dpi
        self.contrasena = contrasena
        self.cargo = cargo
        self.nombre = nombre