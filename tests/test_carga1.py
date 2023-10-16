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
    
    @task
    def login_with_csrf(self):
        # Realizar el inicio de sesión y obtener el token CSRF
        response = self.client.get("https://portal-electronico.onrender.com/logint")  # Ajusta la URL de inicio de sesión según tu aplicación
        csrf_token = self.extract_csrf_token(response)

        if csrf_token: 
            self.client.post("/logint", data=dict(dpi='1234545', contrasena='david123', csrf_token=csrf_token))  # Ajusta la URL de inicio de sesión

    