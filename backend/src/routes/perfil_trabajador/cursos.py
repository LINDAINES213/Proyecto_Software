from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
cursos_bp = Blueprint('cursos_blueprint', __name__)

@cursos_bp.route('/cursos')
@login_required
def cursos():
    return render_template('cursos.html')

@cursos_bp.route('/cursos2', methods=['POST'])
@login_required
def cursos2():
    try:
        id_curso = request.form['id_curso']
        nombre = request.form['nombre']
        maestro = request.form['maestro']
        salon = request.form['salon']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO curso VALUES (%s, %s, %s, %s, %s, %s)""", 
                           (id_curso, nombre, maestro, salon, hora_inicio, hora_fin))
            connection.commit()  
        return redirect('/cursos3')
    except Exception as ex:
        return render_template('cursos.html')

@cursos_bp.route('/cursos2/<id>/edit', methods=['GET', 'POST'])
@login_required
def editar_curso(id):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM curso WHERE id_curso = %s", (id,))
            cur = cursor.fetchone()

        if cur:
            return render_template('editar_curso.html', cur=cur)
        else:
            return 'Curso no encontrado'

    elif request.method == 'POST':
        # Actualizar los datos del trabajador en la base de datos
        id_curso = request.form['id_curso']
        nombre = request.form['nombre']
        maestro = request.form['maestro']
        salon = request.form['salon']
        hora_inicio = request.form['hora_inicio']
        hora_final = request.form['hora_fin']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE curso SET
                nombre = %s,
                maestro = %s,
                salon = %s,
                hora_inicio = %s,
                hora_fin = %s
                WHERE id_curso = %s
            """, (nombre, maestro, salon, hora_inicio, hora_final, id_curso))
            connection.commit()

        return redirect('/cursos3')
    
@cursos_bp.route('/cursos2/<id>/delete', methods=['GET', 'POST'])
@login_required
def eliminar_curso(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM curso WHERE id_curso = %s", (id,))
                connection.commit()

            flash('El curso ha sido eliminado exitosamente.', 'success')
            return redirect('/cursos3')

        return render_template('eliminar_curso.html', curso_id=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el curso.', 'error')
        return redirect('/cursos3')

@cursos_bp.route('/cursos3')
@login_required
def cursos3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT id_curso, nombre, CONCAT(t.nombres,' ', t.apellidos) AS maestro, salon, hora_inicio, hora_fin FROM curso
                        LEFT JOIN trabajadores t ON t.dpi = curso.maestro
                        ORDER BY id_curso ASC""")
        rows = cursor.fetchall()
        return render_template('cursos3.html', rows=rows)
