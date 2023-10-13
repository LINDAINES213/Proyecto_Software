from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
horarios_bp = Blueprint('horarios_blueprint', __name__)

@horarios_bp.route('/horario')
@login_required
def horarios():
    return render_template('admin/horario.html')

@horarios_bp.route('/horario2', methods=['POST'])
@login_required
def horario2():
    try:
        id_horarios = request.form['id_horarios']
        id_curso = request.form['id_curso']
        seccion = request.form['seccion']
        hora_fin = request.form['hora_fin']
        hora_inicio = request.form['hora_inicio']
        dia = request.form['dia']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO horarios VALUES (%s, %s, %s, %s, %s, %s)""",
                           (id_horarios,id_curso,seccion, hora_fin, hora_inicio,dia))
            connection.commit()
        return redirect('/horario3')
    except Exception as ex:
        connection.rollback()
        flash('Error, intente nuevamente')
        return redirect('/horario')

@horarios_bp.route('/horario2/<id>/edit', methods=['GET', 'POST'])
@login_required
def editar_horario(id):
    try:
        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM horarios WHERE id_horarios = %s", (id,))
                hor = cursor.fetchone()

            if hor:
                return render_template('admin/editar_horario.html', hor=hor)
            else:
                return 'horario no encontrado'

        elif request.method == 'POST':
            id_horarios = request.form['id_horarios']
            id_curso = request.form['id_curso']
            seccion = request.form['seccion']
            hora_fin = request.form['hora_fin']
            hora_inicio = request.form['hora_inicio']
            dia = request.form['dia']

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE horarios SET
                    id_curso = %s,
                    seccion = %s,
                    hora_fin = %s,
                    hora_inicio = %s,
                    dia = %s
                    WHERE id_horarios = %s
                """, (id_curso, seccion, hora_fin, hora_inicio, dia, id_horarios))
                connection.commit()
            return redirect('/horario3')
    except Exception as ex:
        connection.rollback()
        flash('Error, intente nuevamente')
        return redirect('/horario')


@horarios_bp.route('/horario2/<id>/delete', methods=['GET', 'POST'])
@login_required
def eliminar_horarios(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM horarios WHERE id_horarios = %s", (id,))
                connection.commit()
            return redirect('/horario3')

        return render_template('admin/eliminar_horario.html', id_horarios=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el horario.', 'error')
        connection.rollback()
        return redirect('/horario')

@horarios_bp.route('/horario3')
@login_required
def cursos3():
    with connection.cursor() as cursor:
        cursor.execute("""select * from horarios
                        group by id_horarios,dia
                        order by hora_inicio""")
        rows = cursor.fetchall()
    return render_template('admin/horario3.html', rows=rows)
