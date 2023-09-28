import uuid
from concurrent.futures import ThreadPoolExecutor

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import unittest
from app import app, get_cargo_from_database
from database import db
import re
import json

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

    #API_URL = "http://127.0.0.1:5000/cursos"

    def create_course(self):
        # Generar un ID único para cada curso
        login_page_response = self.app.get('/logint')
        csrf_token = self.extract_csrf_token(login_page_response)
        self.app.post('/logint', data=dict(dpi='1234545', contrasena='david123', csrf_token=csrf_token), follow_redirects=True)
        self.app.get('/cursos')
        id_curso = str(uuid.uuid4())
        response = self.app.post('/cursos', data=dict(id_curso=id_curso, curso='Curso de Prueba', maestro='57463922', csrf_token=csrf_token))
        self.assertEqual(response.status_code, 200)
        
        
        '''try:
            response = self.app.post('/cursos', data=dict(id_curso=id_curso, curso='Curso de Prueba', maestro='57463922', csrf_token=csrf_token))
            #self.assertEqual(response.status_code, 200)
            response.raise_for_status()  # Verificar si la solicitud fue exitosa
            #self.assertTrue(response.status_code == 200, f"Failed to create a course. Status code: {response.status_code}")
            print(f"Failed to create a course. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to create a course: {e}")'''

    '''@pytest.mark.parametrize("i", range(10))  # Ejecutar la función 50 veces en paralelo
    def test_create_courses_in_parallel(self):
        self.create_course()'''
        
