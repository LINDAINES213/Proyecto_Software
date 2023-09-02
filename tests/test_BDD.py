import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
import re
from pytest_bdd import scenarios, given, when, then
import unittest
from app import app
from database import db

scenarios('BDD.feature')

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.connection = db.get_connection()
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def extract_csrf_token(self, response):
        # Extraer el token CSRF del HTML de la respuesta utilizando expresiones regulares
        match = re.search(r'<input type="hidden" name="csrf_token" value="([^"]+)', response.data.decode())
        if match:
            return match.group(1)
        return None

    @given("que estoy autenticado como secretario")
    def test_autenticado_como_secretario(self):
        login_page_response = self.app.get('/logint')
        csrf_token = self.extract_csrf_token(login_page_response)

        response = self.app.post('/logint', data=dict(dpi='123456789101', contrasena='juan123', csrf_token=csrf_token), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        

    @when('lleno los campos de título y contenido de la circular')
    def test_llenar_campos_de_circular(self):
        login_page_response = self.app.get('/logint')
        csrf_token = self.extract_csrf_token(login_page_response)

        self.app.post('/logint', data=dict(dpi='123456789101', contrasena='juan123', csrf_token=csrf_token), follow_redirects=True)
        
        self.app.get('/crearcircularese')
        response = self.app.post('/crearcircularese', data=dict(titulo='Test Circular', contenido='This is a test circular', csrf_token=csrf_token), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        

    @then('debería ser redirigido a la página de ver circulares')
    def test_redirigido_a_ver_circulares(self):
        # Obtener la página de inicio de sesión para extraer el token CSRF
        login_page_response = self.app.get('/logint')
        csrf_token = self.extract_csrf_token(login_page_response)

        self.app.post('/logint', data=dict(dpi='123456789101', contrasena='juan123', csrf_token=csrf_token), follow_redirects=True)
    
        response = self.app.get('/vercircularesE')
        self.assertEqual(response.status_code, 200)

    
