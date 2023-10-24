from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
crearEstudiante_bp = Blueprint('crearEstudiante_blueprint', __name__)

@crearEstudiante_bp.route('/crearUsuario')
@login_required
def inicio():
    return render_template('admin/crearuser.html')


@crearEstudiante_bp.route('/crearEstudiante', methods=['GET','POST'])
@login_required
def crearEstudiante():
    if request.method == 'POST':
        id_estudiante = request.form['id_estudiante']
        contrasena = request.form['contrasena']

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM estudiantes WHERE id_estudiante = %s", (id_estudiante,))
            user = cursor.fetchone()

            if user:
                # El DPI existe en la base de datos
                with connection.cursor() as cursor:
                    cursor.execute("""INSERT INTO usuarios.userestudiantes (id_estudiante, contrasena)
                                    VALUES (%s, %s)""", (id_estudiante, contrasena))
                    connection.commit()
                cursor.close()
                flash("Usuario creado exitosamente!")
                return render_template('admin/crearEstudiante.html')
            else:
                # El DPI no existe en la base de datos
                flash('ID inexistente', 'error')
                return render_template('admin/crearEstudiante.html')
    else:
        return render_template('admin/crearEstudiante.html')    