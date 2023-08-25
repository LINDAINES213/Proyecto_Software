from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from src.database.db import get_connection


connection = get_connection()
estudiantes_bp = Blueprint('estudiantes_blueprint', __name__)

@estudiantes_bp.route('/estudiantes')
@login_required
def estudiantes():
    return render_template('admin/estudiantes.html')

@estudiantes_bp.route('/estudiantes2', methods=['POST'])
@login_required
def estudiantes2():
    try:
        id_estudiante = request.form['id_estudiante']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        edad = request.form['edad']
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
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO estudiantes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (id_estudiante, nombres, apellidos, fecha_nacimiento, edad, grado, seccion, curso1, curso2, curso3, curso4, curso5, curso6, curso7, curso8, curso9, curso10))
            connection.commit()  
        return redirect('/estudiantes3')
    except Exception as ex:
        return render_template('admin/estudiantes.html')
    
@estudiantes_bp.route('/estudiantes2/<id>/edit', methods=['GET', 'POST'])
@login_required
def editar_estudiante(id):
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

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE estudiantes SET
                nombres = %s,
                apellidos = %s,
                fecha_nacimiento = %s,
                edad =%s,
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
                curso10 = %s
                WHERE id_estudiante = %s
            """, (nombres, apellidos, fecha_nacimiento, edad, grado, seccion, curso1, curso2, curso3, curso4, curso5, curso6, curso7, curso8, curso9, curso10, id_estudiante))
            connection.commit()

        return redirect('/estudiantes3')
    
@estudiantes_bp.route('/estudiantes2/<id>/delete', methods=['GET', 'POST'])
@login_required
def eliminar_estudiante(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM estudiantes WHERE id_estudiante = %s", (id,))
                connection.commit()

            flash('El Estudiante ha sido eliminado exitosamente.', 'success')
            return redirect('/estudiantes3')

        return render_template('admin/eliminar_estudiante.html', id_estudiante=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el trabajador.', 'error')
        return redirect('/estudiantes3')

@estudiantes_bp.route('/estudiantes3')
@login_required
def estudiantes3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM estudiantes
                        ORDER BY id_estudiante ASC""")
        rows = cursor.fetchall()
        return render_template('admin/estudiantes3.html', rows=rows)