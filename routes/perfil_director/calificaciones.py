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

@calificaciones_bp.route('/calificaciones2/<id>/edit', methods=['GET', 'POST'])
@login_required
def editar_calificacion(id):
    try:
        if request.method == 'GET':
            # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM calificaciones WHERE id_estudiante = %s", (id,))
                calificaciones = cursor.fetchone()

            if calificaciones:
                return render_template('director/editar_calificaciones.html', calificaciones=calificaciones)
            else:
                return 'Calificación no encontrada'

        elif request.method == 'POST':
            # Actualizar los datos del trabajador en la base de datos
            id_estudiante = request.form['id_estudiante']
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            grado = request.form['grado']
            seccion = request.form['seccion']
            curso1 = request.form['curso1']
            curso2 = request.form['curso2']
            curso3 = request.form['curso3']
            curso4 = request.form['curso4']
            curso5 = request.form['curso5']
            curso6 = request.form['curso6']
            curso7 = request.form['curso7']
            curso8 = request.form['curso8']
            curso9 = request.form['curso9']
            curso10 = request.form['curso10']
            promedio = request.form['promedio']

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE calificaciones SET
                    nombres = %s,
                    apellidos = %s,
                    grado = %s,
                    seccion = %s,
                    notaCurso1 = %s,
                    notaCurso2 = %s,
                    notaCurso3 = %s,
                    notaCurso4 = %s,
                    notaCurso5 = %s,
                    notaCurso6 = %s,
                    notaCurso7 = %s,
                    notaCurso8 = %s,
                    notaCurso9 = %s,
                    notaCurso10 = %s,
                    promedio = %s
                    WHERE id_estudiante = %s
                """, (nombres, apellidos, grado, seccion, curso1, curso2, curso3, curso4, curso5, curso6, curso7, curso8, curso9, curso10, promedio, id_estudiante))
                connection.commit()

            return redirect('/calificaciones3')
        
    except Exception as ex:
        connection.rollback()
        flash('Error, intente nuevamente')
        return redirect('/calificaciones')