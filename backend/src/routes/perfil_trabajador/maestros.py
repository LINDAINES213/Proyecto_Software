from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
maestros_bp = Blueprint('maestros_blueprint', __name__)

@maestros_bp.route('/maestros')
@login_required
def maestros():
    return render_template('maestros.html')

@maestros_bp.route('/maestros2', methods=['POST'])
@login_required
def mestros2():
    try:
        dpi = request.form['dpi']
        curso_1 = request.form['curso_1']
        curso_2 = request.form['curso_2']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO maestros VALUES (%s, %s, %s)""", 
                           (dpi, curso_1, curso_2))
            connection.commit()  
        return redirect('/maestros3')
    except Exception as ex:
        return render_template('maestros.html')

@maestros_bp.route('/maestros2/<dpi>/edit', methods=['GET', 'POST'])
@login_required
def editar_maestro(dpi):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM maestros WHERE dpi = %s", (dpi,))
            maestro = cursor.fetchone()

        if maestro:
            return render_template('editar_maestro.html', maestro=maestro)
        else:
            return 'Maestro no encontrado'

    elif request.method == 'POST':
        # Actualizar los datos del trabajador en la base de datos
        dpi = request.form['dpi']
        curso_1 = request.form['curso_1']
        curso_2 = request.form['curso_2']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE maestros SET
                curso_1 = %s,
                curso_2 = %s
                WHERE dpi = %s
            """, (curso_1, curso_2, dpi))
            connection.commit()

        return redirect('/maestros3')
    
@maestros_bp.route('/maestros2/<dpi>/delete', methods=['GET', 'POST'])
@login_required
def eliminar_maestro(dpi):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM maestros WHERE dpi = %s", (dpi,))
                connection.commit()

            flash('El maestro ha sido eliminado exitosamente.', 'success')
            return redirect('/maestros3')

        return render_template('eliminar_maestro.html', maestro_dpi=dpi)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el maestro.', 'error')
        return redirect('/maestros3')

@maestros_bp.route('/maestros3')
@login_required
def mestros3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT t.dpi, CONCAT(t.nombres,' ', t.apellidos) AS maestro, curso_1, curso_2 FROM maestros
                        LEFT JOIN trabajadores t ON t.dpi = maestros.dpi
                        ORDER BY dpi ASC""")
        rows = cursor.fetchall()
        return render_template('maestros3.html', rows=rows)