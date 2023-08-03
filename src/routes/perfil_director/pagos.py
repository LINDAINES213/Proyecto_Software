from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
pagos_bp = Blueprint('pagos_blueprint', __name__)

@pagos_bp.route('/pagoP')
@login_required
def pagoP():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM trabajadores
                        ORDER BY dpi ASC""")
        rows = cursor.fetchall()
        return render_template('director/pagoP.html', rows=rows)
    
@pagos_bp.route('/pagoC')
@login_required
def pagoC():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM estudiantes
                        ORDER BY id_estudiante ASC""")
        rows = cursor.fetchall()
        return render_template('director/pagoC.html', rows=rows)