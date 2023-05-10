from flask import Flask, render_template, request, redirect, url_for, flash
from database.db import get_connection
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from config import config


app = Flask(__name__)
csrf = CSRFProtect(app)
connection = get_connection()
CORS(app)

@app.before_request
def override_method():
    if request.form.get('_method'):
        request.environ['REQUEST_METHOD'] = request.form['_method'].upper()

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/trabajadores')
def trabajadores():
    return render_template('trabajadores.html')

@app.route('/trabajadores2', methods=['POST'])
def trabajadores2():
    try:
        id_trabajador = request.form['id_trabajador']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cargo = request.form['cargo']
        salario = request.form['salario']
        metodo_pago = request.form['metodo_pago']
        bonus = request.form['bonus']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO trabajador VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                           (id_trabajador, nombres, apellidos, cargo, salario, metodo_pago, bonus))
            connection.commit()  
        return redirect('/trabajadores3')
    except Exception as ex:
        return render_template('trabajadores.html')

@app.route('/trabajadores2/<id>/edit', methods=['GET', 'POST'])
def edit_worker(id):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trabajador WHERE id_trabajador = %s", (id,))
            worker = cursor.fetchone()

        if worker:
            return render_template('editar_trabajador.html', worker=worker)
        else:
            return 'Trabajador no encontrado'

    elif request.method == 'POST':
        # Actualizar los datos del trabajador en la base de datos
        id_trabajador = request.form['id_trabajador']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cargo = request.form['cargo']
        salario = request.form['salario']
        metodo_pago = request.form['metodo_pago']
        bonus = request.form['bonus']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE trabajador SET
                nombres = %s,
                apellidos = %s,
                cargo = %s,
                salario = %s,
                metodo_pago = %s,
                bonus = %s
                WHERE id_trabajador = %s
            """, (nombres, apellidos, cargo, salario, metodo_pago, bonus, id_trabajador))
            connection.commit()

        return redirect('/trabajadores3')
    
@app.route('/trabajadores2/<id>/delete', methods=['GET', 'POST'])
def delete_worker(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM trabajador WHERE id_trabajador = %s", (id,))
                connection.commit()

            flash('El trabajador ha sido eliminado exitosamente.', 'success')
            return redirect('/trabajadores3')

        return render_template('eliminar_trabajador.html', worker_id=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el trabajador.', 'error')
        return redirect('/trabajadores3')

@app.route('/trabajadores3')
def trabajores3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM trabajador
                        ORDER BY id_trabajador ASC""")
        rows = cursor.fetchall()
        return render_template('trabajores3.html', rows=rows)


@app.route('/maestros')
def maestros():
    return render_template('maestros.html')

@app.route('/maestros2', methods=['POST'])
def mestros2():
    try:
        id_maestro = request.form['id_maestro']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        curso = request.form['curso']
        salario = request.form['salario']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO maestro VALUES (%s, %s, %s, %s, %s)""", 
                           (id_maestro, nombres, apellidos, curso, salario))
            connection.commit()  
        return redirect('/maestros3')
    except Exception as ex:
        return render_template('maestros.html')

@app.route('/maestros2/<id>/edit', methods=['GET', 'POST'])
def editar_maestro(id):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM maestro WHERE id_maestro = %s", (id,))
            maestro = cursor.fetchone()

        if maestro:
            return render_template('editar_maestro.html', maestro=maestro)
        else:
            return 'Maestro no encontrado'

    elif request.method == 'POST':
        # Actualizar los datos del trabajador en la base de datos
        id_maestro = request.form['id_maestro']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        curso = request.form['curso']
        salario = request.form['salario']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE maestro SET
                nombres = %s,
                apellidos = %s,
                curso = %s,
                salario = %s
                WHERE id_maestro = %s
            """, (nombres, apellidos, curso, salario, id_maestro))
            connection.commit()

        return redirect('/maestros3')
    
@app.route('/maestros2/<id>/delete', methods=['GET', 'POST'])
def eliminar_maestro(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM maestro WHERE id_maestro = %s", (id,))
                connection.commit()

            flash('El maestro ha sido eliminado exitosamente.', 'success')
            return redirect('/maestros3')

        return render_template('eliminar_maestro.html', maestro_id=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el maestro.', 'error')
        return redirect('/maestros3')

@app.route('/maestros3')
def mestros3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM maestro
                        ORDER BY id_maestro ASC""")
        rows = cursor.fetchall()
        return render_template('maestros3.html', rows=rows)



@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/cursos2', methods=['POST'])
def cursos2():
    try:
        id_curso = request.form['id_curso']
        nombre = request.form['nombre']
        salon = request.form['salon']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO curso VALUES (%s, %s, %s, %s, %s)""", 
                           (id_curso, nombre, salon, hora_inicio, hora_fin))
            connection.commit()  
        return redirect('/cursos3')
    except Exception as ex:
        return render_template('cursos.html')

@app.route('/cursos2/<id>/edit', methods=['GET', 'POST'])
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
        salon = request.form['salon']
        hora_inicio = request.form['hora_inicio']
        hora_final = request.form['hora_fin']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE curso SET
                nombre = %s,
                salon = %s,
                hora_inicio = %s,
                hora_fin = %s
                WHERE id_curso = %s
            """, (nombre, salon, hora_inicio, hora_final, id_curso))
            connection.commit()

        return redirect('/cursos3')
    
@app.route('/cursos2/<id>/delete', methods=['GET', 'POST'])
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

@app.route('/cursos3')
def cursos3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM curso
                        ORDER BY id_curso ASC""")
        rows = cursor.fetchall()
        return render_template('cursos3.html', rows=rows)

def page_not_found(error):
    return "<h1>Not found page</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()