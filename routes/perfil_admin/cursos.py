from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
cursos_bp = Blueprint('cursos_blueprint', __name__)

@cursos_bp.route('/cursos')
@login_required
def cursos():
    return render_template('admin/cursos.html')

@cursos_bp.route('/cursos2', methods=['POST'])
@login_required
def cursos2():
    try:
        id_curso = request.form['id_curso']
        curso = request.form['curso']
        maestro = request.form['maestro']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO curso VALUES (%s, %s, %s)""", 
                           (id_curso, curso, maestro))
            connection.commit()  
        return redirect('/cursos3')
    except Exception as ex:
        connection.rollback()
        flash('Error, intente nuevamente')
        return redirect('/cursos')

@cursos_bp.route('/cursos2/<id>/edit', methods=['GET', 'POST'])
@login_required
def editar_curso(id):
    try:
        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM curso WHERE id_curso = %s", (id,))
                cur = cursor.fetchone()

            if cur:
                return render_template('admin/editar_curso.html', cur=cur)
            else:
                return 'Curso no encontrado'

        elif request.method == 'POST':
            id_curso = request.form['id_curso']
            curso = request.form['curso']
            maestro = request.form['maestro']

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE curso SET
                    curso = %s,
                    maestro = %s
                    WHERE id_curso = %s
                """, (curso, maestro, id_curso))
                connection.commit()
        return redirect('/cursos3')
    except Exception as ex:
        connection.rollback()
        flash('Error, intente nuevamente')
        return redirect('/cursos')
    
    
@cursos_bp.route('/cursos2/<id>/delete', methods=['GET', 'POST'])
@login_required
def eliminar_curso(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM curso WHERE id_curso = %s", (id,))
                connection.commit()
            return redirect('/cursos3')

        return render_template('admin/eliminar_curso.html', curso_id=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el curso.', 'error')
        connection.rollback()
        return redirect('/cursos')

@cursos_bp.route('/cursos3')
@login_required
def cursos3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT id_curso, curso, m.nombre FROM curso
                        LEFT JOIN maestros m ON m.dpi = curso.maestro
                        ORDER BY id_curso ASC""")
        rows = cursor.fetchall()
    return render_template('admin/cursos3.html', rows=rows)
