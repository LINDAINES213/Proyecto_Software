from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
maestros_bp = Blueprint('maestros_blueprint', __name__)

@maestros_bp.route('/maestros')
@login_required
def maestros():
    return render_template('admin/maestros.html')

@maestros_bp.route('/maestros2', methods=['POST'])
@login_required
def maestros2():
    try:
        dpi = request.form['dpi']

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO maestros (dpi) VALUES (%s)", (dpi,))
            connection.commit()  
        return redirect('/maestros3')
    except Exception as ex:
        connection.rollback()  # Revertir la transacción en caso de error
        flash('Error, verifique que el DPI exista en la base de datos')
        return redirect('/maestros')

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

        return render_template('admin/eliminar_maestro.html', maestro_dpi=dpi)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el maestro.', 'error')
        return redirect('/maestros3')

@maestros_bp.route('/maestros3')
@login_required
def maestros3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM maestros
                        ORDER BY dpi ASC""")
        rows = cursor.fetchall()
        return render_template('admin/maestros3.html', rows=rows)
