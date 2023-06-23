from flask import Blueprint, redirect, render_template, request, flash, url_for, send_file
from flask_login import login_required, logout_user
from database.db import get_connection


connection = get_connection()
crearUsuario_bp = Blueprint('crearUsuario_blueprint', __name__)

@crearUsuario_bp.route('/crearUsuario', methods=['GET','POST'])
def crearUsuario():
    try:
        if request.method == 'POST':
            dpi = request.form['dpi']
            contrasena = request.form['contrasena']

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO usuarios.user (dpi, contrasena)
                                VALUES (%s, %s)""", (dpi, contrasena))
                connection.commit()
            cursor.close()
            return render_template('confirmaciones.html')
        else:
            flash("El DPI ingresado no existe en la base de datos")
            return render_template('admin/crearUsuario.html')
        
    except Exception as ex:
        return render_template('admin/crearUsuario.html')