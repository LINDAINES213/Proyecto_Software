from flask import Blueprint, redirect, render_template, request, flash, url_for, send_file
from flask_login import login_required, logout_user
from database.db import get_connection


connection = get_connection()
crearUsuario_bp = Blueprint('crearUsuario_blueprint', __name__)

@crearUsuario_bp.route('/crearUsuario')
@login_required
def inicio():
    return render_template('admin/crearuser.html')

@crearUsuario_bp.route('/crearTrabajador', methods=['GET','POST'])
@login_required
def crearTrabajador():
    if request.method == 'POST':
        dpi = request.form['dpi']
        contrasena = request.form['contrasena']

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trabajadores WHERE dpi = %s", (dpi,))
            user = cursor.fetchone()

            if user:
                # El DPI existe en la base de datos
                with connection.cursor() as cursor:
                    cursor.execute("""INSERT INTO usuarios.user (dpi, contrasena)
                                    VALUES (%s, %s)""", (dpi, contrasena))
                    connection.commit()
                cursor.close()
                flash("Usuario creado exitosamente!")
                return render_template('admin/crearTrabajador.html')
            else:
                # El DPI no existe en la base de datos
                flash('DPI inexistente', 'error')
                return render_template('admin/crearTrabajador.html')
    else:
        return render_template('admin/crearTrabajador.html')
    

@crearUsuario_bp.route('/crearEstudiante', methods=['GET','POST'])
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