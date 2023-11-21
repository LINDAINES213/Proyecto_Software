from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection

connection = get_connection()
usuarios_bp = Blueprint('usuarios_blueprint', __name__)

@usuarios_bp.route('/verusuarios')
@login_required
def verusuarios():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT dpi, contrasena, cargo, nombre FROM usuarios.user
                       ORDER BY dpi ASC""")
        rows = cursor.fetchall()
        return render_template('admin/verusuarios.html', rows=rows)
    
@usuarios_bp.route('/verusuariosestudiantes')
@login_required
def verusuariosestudiantes():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM usuarios.userestudiantes
                       ORDER BY id_estudiante ASC""")
        rows = cursor.fetchall()
        return render_template('admin/verusuariosestudiantes.html', rows=rows)
