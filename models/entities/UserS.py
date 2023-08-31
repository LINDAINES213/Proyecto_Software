from flask_login import UserMixin

class UserS(UserMixin):

    def __init__(self, id, id_estudiante, contrasena, enombre="", grado="", seccion="") -> None:
        self.id = id
        self.id_estudiante = id_estudiante
        self.contrasena = contrasena
        self.enombre = enombre
        self.grado = grado
        self.seccion = seccion