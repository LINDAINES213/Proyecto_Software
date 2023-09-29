from locust import HttpUser, task, between
import re
import uuid

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Intervalo de tiempo entre solicitudes

    def extract_csrf_token(self, response):
        # Extraer el token CSRF del HTML de la respuesta utilizando expresiones regulares
        match = re.search(r'<input type="hidden" name="csrf_token" value="([^"]+)', response.text)
        if match:
            return match.group(1)
        return None
    

    def login_with_csrf(self):
        # Realizar el inicio de sesión y obtener el token CSRF
        response = self.client.get("/logint")  # Ajusta la URL de inicio de sesión según tu aplicación
        csrf_token = self.extract_csrf_token(response)

        if csrf_token: 
            self.client.post("/logint", data=dict(dpi='1234545', contrasena='david123', csrf_token=csrf_token))  # Ajusta la URL de inicio de sesión

    @task
    def perform_actions_with_csrf(self):
        # Iniciar sesión con CSRF
        self.login_with_csrf()

        # Realizar otras acciones que requieran CSRF, como insertar cursos
        csrf_token = self.extract_csrf_token(self.client.get("/estudiantes"))  # Ajusta la URL según tu aplicación
        if csrf_token:
            id_estudiante = str(uuid.uuid4())
            self.client.post("/estudiantes2", data=dict(id_estudiante=id_estudiante, nombres='Nombre', apellidos='Apellido', fecha_nacimiento='08/31/2003', edad='20', grado='SS7', seccion='SS7-A', csrf_token=csrf_token))
