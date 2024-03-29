from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
pagosdirector_bp = Blueprint('pagosdirector_blueprint', __name__)

@pagosdirector_bp.route('/pagoPD')
@login_required
def pagoP():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM trabajadores
                        ORDER BY fecha_pago ASC""")
        rows = cursor.fetchall()
        return render_template('director/pagoP.html', rows=rows)
    
@pagosdirector_bp.route('/pagoCD')
@login_required
def pagoC():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT id_estudiante, nombres, apellidos, fecha_nacimiento, grado, seccion FROM estudiantes
                        ORDER BY grado ASC""")
        rows = cursor.fetchall()
        return render_template('director/pagoC.html', rows=rows)
