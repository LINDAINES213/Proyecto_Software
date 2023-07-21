from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
calificaciones_bp = Blueprint('calificaciones_blueprint', __name__)

@calificaciones_bp.route('/calificaciones')
@login_required
def calificaciones():
    return render_template('director/calificaciones.html')

@calificaciones_bp.route('/calificaciones2', methods=['POST'])
@login_required
def calificaciones2():
    try:
        grado = request.form['grado']
        seccion = request.form['seccion']

        with connection.cursor() as cursor:
            cursor.execute("""SELECT * from calificaciones WHERE grado=%s and seccion=%s)""", 
                           (grado, seccion))
            connection.commit()  
        return redirect('/calificaciones3')
    except Exception as ex:
        return render_template('director/calificaciones.html')

@calificaciones_bp.route('/calificaciones2/<id_estudiante>/edit', methods=['GET', 'POST'])
@login_required
def editar_calificacion(id_estudiante):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM calificaciones WHERE id_estudiante = %s", (id_estudiante,))
            calificacion = cursor.fetchone()

        if calificacion:
            return render_template('director/editar_calificacion.html', calificacion=calificacion)
        else:
            return 'Estudiante no encontrado'

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
                curso1 = %s,
                curso2 = %s,
                curso3 = %s,
                curso4 = %s,
                curso5 = %s,
                curso6 = %s,
                curso7 = %s,
                curso8 = %s,
                curso9 = %s,
                curso10 = %s,
                promedio = %s
                WHERE id_estudiante = %s
            """, (nombres, apellidos, grado, seccion, curso1, curso2, curso3, curso4, curso5, curso6, curso7, curso8, curso9, curso10, promedio, id_estudiante))
            connection.commit()

        return redirect('/calificaciones3')

@calificaciones_bp.route('/calificaciones3')
@login_required
def calificaciones3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT id_estudiante, CONCAT(nombres,' ', apellidos) AS estudiante, grado, seccion,
                        curso1, curso2, curso3, curso4, curso5, curso6, curso7, curso8, curso9, curso10, promedio FROM calificaciones
                        ORDER BY id_estudiante ASC""")
        rows = cursor.fetchall()
        return render_template('director/calificaciones3.html', rows=rows)