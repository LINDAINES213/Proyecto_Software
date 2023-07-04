from flask import Blueprint, redirect, render_template, request, flash, url_for, send_file
from flask_login import login_required, logout_user
from database.db import get_connection


connection = get_connection()
crearUsuario_bp = Blueprint('crearUsuario_blueprint', __name__)

@crearUsuario_bp.route('/crearUsuario', methods=['GET','POST'])
def crearUsuario():
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
                return render_template('admin/crearUsuario.html')
            else:
                # El DPI no existe en la base de datos
                flash('DPI o contraseña incorrecta', 'error')
                return render_template('admin/crearUsuario.html')
    else:
        return render_template('admin/crearUsuario.html')



    '''if request.method == 'POST':
        dpi = request.form['dpi']
        contrasena = request.form['contrasena']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO usuarios.user (dpi, contrasena)
                                VALUES (%s, %s)""", (dpi, contrasena))
            connection.commit()
        cursor.close()
        return render_template('confirmaciones.html')
    else:
        return render_template('admin/crearUsuario.html')'''
    
    