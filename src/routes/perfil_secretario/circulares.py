from flask import Blueprint, redirect, render_template, request, flash, url_for, send_file
from flask_login import login_required, logout_user
from database.db import get_connection


connection = get_connection()
circulares_bp = Blueprint('circulares_blueprint', __name__)

@circulares_bp.route('/enviarcirculares', methods=['GET'])
@login_required
def enviarcirculares():
    return render_template('secretario/crearcirculares.html')

@circulares_bp.route('/crearcirculares', methods=['GET', 'POST'])
@login_required
def crearcirculares():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            contenido = request.form['contenido']

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO circulares.poststrabajadores (titulo, contenido) VALUES (%s, %s)", (titulo, contenido))
                connection.commit()
                
                # Cerrar la conexión después de realizar la operación
            cursor.close()
                
            return redirect('/vercirculares')
        except Exception as ex:
            # Manejar la excepción adecuadamente y mostrar un mensaje de error en la plantilla
            flash("Error al crear la circular. Inténtelo de nuevo.", "error")
            connection.close()  # Cerrar la conexión en caso de excepción
            return render_template('secretario/crearcirculares.html')

    # Asegurarse de devolver una respuesta para el caso en que el método sea GET
    return render_template('secretario/crearcirculares.html')


# Vista para mostrar todas las publicaciones
@circulares_bp.route('/vercirculares', methods=['GET'])
@login_required
def vercircular():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM circulares.poststrabajadores ORDER BY creado DESC""")
        rows = cursor.fetchall()
        return render_template('secretario/circulares.html', rows=rows)