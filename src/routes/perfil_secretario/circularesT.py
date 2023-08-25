from flask import Blueprint, redirect, render_template, request, flash, url_for, send_file
from flask_login import login_required, logout_user
from src.database.db import get_connection


connection = get_connection()
circularesT_bp = Blueprint('circularesT_blueprint', __name__)

@circularesT_bp.route('/enviarcirculares', methods=['GET'])
@login_required
def enviarcirculares():
    return render_template('secretario/home.html')

@circularesT_bp.route('/crearcircularest', methods=['GET', 'POST'])
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
                
            return redirect('/vercircularesT')
        except Exception as ex:
            # Manejar la excepción adecuadamente y mostrar un mensaje de error en la plantilla
            flash("Error al crear la circular. Inténtelo de nuevo.", "error")
            connection.close()  # Cerrar la conexión en caso de excepción
            return render_template('secretario/crearcircularesT.html')

    # Asegurarse de devolver una respuesta para el caso en que el método sea GET
    return render_template('secretario/crearcircularesT.html')


# Vista para mostrar todas las publicaciones
@circularesT_bp.route('/vercircularesT', methods=['GET'])
@login_required
def vercircularesT():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM circulares.poststrabajadores ORDER BY creado DESC""")
        rows = cursor.fetchall()
        return render_template('secretario/circularesT.html', rows=rows)