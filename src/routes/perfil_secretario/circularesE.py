from flask import Blueprint, redirect, render_template, request, flash, url_for, send_file
from flask_login import login_required, logout_user
from src.database.db import get_connection


connection = get_connection()
circularesE_bp = Blueprint('circularesE_blueprint', __name__)

@circularesE_bp.route('/crearcircularese', methods=['GET', 'POST'])
@login_required
def crearcircularese():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            contenido = request.form['contenido']

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO circulares.postsestudiantes (titulo, contenido) VALUES (%s, %s)", (titulo, contenido))
                connection.commit()
                
            # Cerrar la conexión después de realizar la operación
            cursor.close()
                
            return redirect('/vercircularesE')
        except Exception as ex:
            # Manejar la excepción adecuadamente y mostrar un mensaje de error en la plantilla
            flash("Error al crear la circular. Inténtelo de nuevo.", "error")
            connection.close()  # Cerrar la conexión en caso de excepción
            return render_template('secretario/crearcircularesE.html')

    # Asegurarse de devolver una respuesta para el caso en que el método sea GET
    return render_template('secretario/crearcircularesE.html')


# Vista para mostrar todas las publicaciones
@circularesE_bp.route('/vercircularesE', methods=['GET'])
@login_required
def vercircularesE():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM circulares.postsestudiantes ORDER BY creado DESC""")
        rows = cursor.fetchall()
        return render_template('secretario/circularesE.html', rows=rows)