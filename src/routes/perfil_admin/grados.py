from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
grados_bp = Blueprint('grados_blueprint', __name__)

@grados_bp.route('/grados')
@login_required
def grados():
    return render_template('admin/grados.html')

@grados_bp.route('/grados2', methods=['POST'])
@login_required
def grados2():
    try:
        id_grado = request.form['id_grado']
        grado = request.form['grado']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO grado VALUES (%s, %s)""", 
                           (id_grado, grado))
            connection.commit()  
        return redirect('/grados3')
    except Exception as ex:
        return render_template('admin/grados.html')

@grados_bp.route('/grados2/<id>/edit', methods=['GET', 'POST'])
@login_required
def editar_grado(id):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM grado WHERE id_grado = %s", (id,))
            grado = cursor.fetchone()

        if grado:
            return render_template('admin/editar_grado.html', grado=grado)
        else:
            return 'Grado no encontrado'

    elif request.method == 'POST':
        # Actualizar los datos del salon en la base de datos
        id_grado = request.form['id_grado']
        grado = request.form['grado']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE grado SET
                grado = %s
                WHERE id_grado = %s
            """, (grado, id_grado))
            connection.commit()

        return redirect('/grados3')
    
@grados_bp.route('/grados2/<id>/delete', methods=['GET', 'POST'])
@login_required
def eliminar_grado(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM grado WHERE id_grado = %s", (id,))
                connection.commit()

            flash('El salon ha sido eliminado exitosamente.', 'success')
            return redirect('/grados3')

        return render_template('admin/eliminar_grado.html', id_grado=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el salon.', 'error')
        return redirect('/grados3')

@grados_bp.route('/grados3')
@login_required
def grados3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM grado
                        ORDER BY id_grado ASC""")
        rows = cursor.fetchall()
        return render_template('admin/grados3.html', rows=rows)