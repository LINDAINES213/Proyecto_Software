from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
calificaciones_bp = Blueprint('calificaciones_blueprint', __name__)

@calificaciones_bp.route('/calificaciones')
@login_required
def calificaciones():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM estudiantes""")
        '''cursor.execute("""SELECT id_estudiante, nombres, apellidos, grado, seccion,
                        curso1, curso2, curso3, curso4, curso5, curso6, curso7, curso8, curso9, curso10, promedio FROM calificaciones
                        ORDER BY grado ASC""")'''
        rows = cursor.fetchall()
        return render_template('director/calificaciones3.html', rows=rows)