from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
secciones_bp = Blueprint('secciones_blueprint', __name__)

@secciones_bp.route('/secciones')
@login_required
def secciones():
    return render_template('admin/secciones.html')

@secciones_bp.route('/secciones2', methods=['POST'])
@login_required
def secciones2():
    try:
        id_grado = request.form['id_grado']
        id_seccion = request.form['id_seccion']
        seccion = request.form['seccion']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO seccion VALUES (%s, %s, %s)""", (id_grado, id_seccion, seccion))
            connection.commit()  
        return redirect('/secciones3')
    except Exception as ex:
        connection.rollback()
        flash('Error, intente nuevamente')
        return redirect('/secciones')

@secciones_bp.route('/secciones2/<id>/edit', methods=['GET', 'POST'])
@login_required
def editar_seccion(id):
    try:
        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM seccion WHERE id_seccion = %s", (id,))
                seccion = cursor.fetchone()

            if seccion:
                return render_template('admin/editar_seccion.html', seccion=seccion)
            else:
                return 'Seccion no encontrado'

        elif request.method == 'POST':
            id_grado = request.form['id_grado']
            id_seccion = request.form['id_seccion']
            seccion = request.form['seccion']

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE seccion SET
                    seccion = %s
                    WHERE id_seccion = %s
                """, (seccion, id_seccion))
                connection.commit()

            return redirect('/secciones3')
    except Exception as ex:
        connection.rollback()
        flash('Error, intente nuevamente')
        return redirect('/secciones')
    
@secciones_bp.route('/secciones2/<id>/delete', methods=['GET', 'POST'])
@login_required
def eliminar_seccion(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM seccion WHERE id_seccion = %s", (id,))
                connection.commit()

            return redirect('/secciones3')

        return render_template('admin/eliminar_seccion.html', id_seccion=id)

    except Exception as ex:
        connection.rollback()
        flash('Ocurrió un error al intentar eliminar el salon.', 'error')
        return redirect('/secciones')

@secciones_bp.route('/secciones3')
@login_required
def secciones3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM seccion ORDER BY id_seccion ASC""")
        rows = cursor.fetchall()
        return render_template('admin/secciones3.html', rows=rows)