from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
calificaciones_bp = Blueprint('calificaciones_blueprint', __name__)

@calificaciones_bp.route('/calificaciones')
@login_required
def calificaciones():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT id_estudiante, nombres, apellidos, grado, seccion,
                        notaCurso1, notaCurso2, notaCurso3, notaCurso4, notaCurso5, notaCurso6, notaCurso7, notaCurso8, notaCurso9, notaCurso10, promedio FROM calificaciones
                        ORDER BY grado ASC""")
        rows = cursor.fetchall()
        return render_template('director/calificaciones3.html', rows=rows)

@calificaciones_bp.route('/estudiantes2/<id>/edit', methods=['GET', 'POST'])
@login_required
def editar_calificacion(id):
    try:
        if request.method == 'GET':
            # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM estudiantes WHERE id_estudiante = %s", (id,))
                estudiante = cursor.fetchone()

            if estudiante:
                return render_template('admin/editar_estudiante.html', estudiante=estudiante)
            else:
                return 'Estudiante no encontrado'

        elif request.method == 'POST':
            # Actualizar los datos del trabajador en la base de datos
            id_estudiante = request.form['id_estudiante']
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            fecha_nacimiento = request.form['fecha_nacimiento']
            edad = request.form['edad']
            grado = request.form['grado']
            seccion = request.form['seccion']

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE estudiantes SET
                    nombres = %s,
                    apellidos = %s,
                    fecha_nacimiento = %s,
                    edad =%s,
                    grado = %s,
                    seccion = %s
                    WHERE id_estudiante = %s
                """, (nombres, apellidos, fecha_nacimiento, edad, grado, seccion, id_estudiante))
                connection.commit()

            return redirect('/estudiantes3')
        
    except Exception as ex:
        connection.rollback()
        flash('Error, intente nuevamente')
        return redirect('/estudiantes')