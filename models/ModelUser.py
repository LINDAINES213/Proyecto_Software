from .entities.User import User
from .entities.UserS import UserS
from database.db import get_connection

class ModelUser():

    @classmethod
    def login(self, connection, user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""SELECT id, dpi, contrasena, cargo, nombre
                                FROM usuarios.user
                                WHERE dpi = '{}' AND contrasena = '{}'""".format(user.dpi, user.contrasena))
                row = cursor.fetchone()

                if row != None:
                    user = User(row[0], row[1], row[2], row[3], row[4])
                    return user
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def loginE(self, connection, user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""SELECT id, id_estudiante, contrasena, enombre, grado, seccion
                                FROM usuarios.userestudiantes
                                WHERE id_estudiante = '{}' AND contrasena = '{}'""".format(user.id_estudiante, user.contrasena))
                row = cursor.fetchone()

                if row != None:
                    user = UserS(row[0], row[1], row[2], row[3], row[4], row[5])
                    return user
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, connection, id):
        try:
            connection = get_connection() 
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, dpi, cargo, nombre FROM usuarios.user WHERE id = '{}'".format(id))
                row = cursor.fetchone()
            
                if row != None:
                    return User(row[0], row[1], row[2], None, row[3])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_idE(self, connection, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, id_estudiante, enombre, grado, seccion FROM usuarios.userestudiantes WHERE id = '{}'".format(id))
                row = cursor.fetchone()
            
                if row != None:
                    return UserS(row[0], row[1], None, row[2], row[3], row[4])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)
        