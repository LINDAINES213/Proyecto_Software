from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
salones_bp = Blueprint('salones_blueprint', __name__)

@salones_bp.route('/salones')
@login_required
def salones():
    return render_template('admin/salones.html')

@salones_bp.route('/salones2', methods=['POST'])
@login_required
def salones2():
    try:
        id_salon = request.form['id_salon']
        salon = request.form['salon']
        aforo = request.form['aforo']
        dpi_maestro = request.form['dpi_maestro']
        grado_asignado = request.form['grado_asignado']
        seccion_asignada = request.form['seccion_asignada']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO salon VALUES (%s, %s, %s, %s, %s, %s)""", 
                           (id_salon, salon, aforo, dpi_maestro, grado_asignado, seccion_asignada))
            connection.commit()  
        return redirect('/salones3')
    except Exception as ex:
        return render_template('admin/salones.html')

@salones_bp.route('/salones2/<id>/edit', methods=['GET', 'POST'])
@login_required
def editar_salon(id):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM salon WHERE id_salon = %s", (id,))
            salon = cursor.fetchone()

        if salon:
            return render_template('admin/editar_salon.html', salon=salon)
        else:
            return 'Salon no encontrado'

    elif request.method == 'POST':
        # Actualizar los datos del salon en la base de datos
        id_salon = request.form['id_salon']
        salon = request.form['salon']
        aforo = request.form['aforo']
        dpi_maestro = request.form['dpi_maestro']
        grado_asignado = request.form['grado_asignado']
        seccion_asignada = request.form['seccion_asignada']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE salon SET
                salon = %s,
                aforo = %s,
                dpi_maestro = %s,
                grado_asignado = %s,
                seccion_asignada = %s
                WHERE id_salon = %s
            """, (salon, aforo, dpi_maestro, grado_asignado, seccion_asignada, id_salon))
            connection.commit()

        return redirect('/salones3')
    
@salones_bp.route('/salones2/<id>/delete', methods=['GET', 'POST'])
@login_required
def eliminar_salon(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM salon WHERE id_salon = %s", (id,))
                connection.commit()

            flash('El salon ha sido eliminado exitosamente.', 'success')
            return redirect('/salones3')

        return render_template('admin/eliminar_salon.html', salon_id=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el salon.', 'error')
        return redirect('/salones3')

@salones_bp.route('/salones3')
@login_required
def salones3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM salon
                        ORDER BY id_salon ASC""")
        rows = cursor.fetchall()
        return render_template('admin/salones3.html', rows=rows)