import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import unittest
from app import app, get_cargo_from_database
from database import db
import re
import json
from app import app

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
    
    
    # Enfoque TDD: Prueba de unidad para la función get_cargo_from_database
    def test_get_cargo_from_database(self):
        dpi = '1234545'
        expected_cargo = 'Coordinador'
        actual_cargo = get_cargo_from_database(dpi)
        assert actual_cargo == expected_cargo, f"Expected cargo: {expected_cargo}, Actual cargo: {actual_cargo}"

    def test_crear_trabajador_usuario_existente(self):
        # Obtener la página de inicio de sesión para extraer el token CSRF
        login_page_response = self.app.get('/logint')
        csrf_token = self.extract_csrf_token(login_page_response)
        self.app.post('/logint', data=dict(dpi='1234545', contrasena='david123', csrf_token=csrf_token), follow_redirects=True)
        
        self.app.get('/crearTrabajador')
        response = self.app.post('/crearTrabajador', data=dict(dpi='111234567891', contrasena='eduardo123', csrf_token=csrf_token))
        self.assertEqual(response.status_code, 200)
        '''
        789101123456 carlos123
        876543210129 fernanda123
        765432101298 sergio123
        321012987654 paola123
        345678910112 laura123
        '''
        



    '''def test_crear_trabajador_usuario_inexistente(self):
        login_page_response = self.app.get('/logint')
        csrf_token = self.extract_csrf_token(login_page_response)
        self.app.post('/logint', data=dict(dpi='1234545', contrasena='david123', csrf_token=csrf_token), follow_redirects=True)
        

        self.app.get('/crearTrabajador')
        response = self.app.post('/crearTrabajador', data=dict(dpi='222', contrasena='ines13', csrf_token=csrf_token))
        self.assertEqual(response.status_code, 400)'''

    
