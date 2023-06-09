from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, logout_user
from database.db import get_connection


connection = get_connection()
trabajadores_bp = Blueprint('trabajadores_blueprint', __name__)


@trabajadores_bp.route('/trabajadores')
@login_required
def trabajadores():
    return render_template('trabajadores.html')

@trabajadores_bp.route('/trabajadores2', methods=['POST'])
@login_required
def trabajadores2():
    try:
        dpi = request.form['dpi']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cargo = request.form['cargo']
        salario = request.form['salario']
        metodo_de_pago = request.form['metodo_de_pago']
        bonus = request.form['bonus']
        fecha_contratacion = request.form['fecha_contratacion']
        fecha_pago = request.form['fecha_pago']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO trabajadores VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (dpi, nombres, apellidos, cargo, salario, metodo_de_pago, bonus, fecha_contratacion, fecha_pago))
            connection.commit()  
        return redirect('/trabajadores3')
    except Exception as ex:
        return render_template('trabajadores.html')

@trabajadores_bp.route('/trabajadores2/<dpi>/edit', methods=['GET', 'POST'])
@login_required
def edit_worker(dpi):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trabajadores WHERE dpi = %s", (dpi,))
            worker = cursor.fetchone()

        if worker:
            return render_template('editar_trabajador.html', worker=worker)
        else:
            return 'Trabajador no encontrado'

    elif request.method == 'POST':
        # Actualizar los datos del trabajador en la base de datos
        dpi = request.form['dpi']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cargo = request.form['cargo']
        salario = request.form['salario']
        metodo_de_pago = request.form['metodo_de_pago']
        bonus = request.form['bonus']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE trabajadores SET
                nombres = %s,
                apellidos = %s,
                cargo = %s,
                salario = %s,
                metodo_de_pago = %s,
                bonus = %s
                WHERE dpi = %s
            """, (nombres, apellidos, cargo, salario, metodo_de_pago, bonus, dpi))
            connection.commit()

        return redirect('/trabajadores3')
    
@trabajadores_bp.route('/trabajadores2/<dpi>/delete', methods=['GET', 'POST'])
@login_required
def delete_worker(dpi):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM trabajadores WHERE dpi = %s", (dpi,))
                connection.commit()

            flash('El trabajador ha sido eliminado exitosamente.', 'success')
            return redirect('/trabajadores3')

        return render_template('eliminar_trabajador.html', worker_dpi=dpi)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el trabajador.', 'error')
        return redirect('/trabajadores3')

@trabajadores_bp.route('/trabajadores3')
@login_required
def trabajores3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM trabajadores
                        ORDER BY dpi ASC""")
        rows = cursor.fetchall()
        return render_template('trabajores3.html', rows=rows)
