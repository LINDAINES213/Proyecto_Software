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
        dpi = request.form['dpi']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cargo = request.form['cargo']
        salario = request.form['salario']
        metodo_de_pago = request.form['metodo_de_pago']
        bonus = request.form['bonus']
        fecha_contratacion = request.form['fecha_contratacion']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO trabajadores VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (dpi, nombres, apellidos, cargo, salario, metodo_de_pago, bonus, fecha_contratacion))
            connection.commit()  
        return redirect('/trabajadores3')
    except Exception as ex:
        return render_template('trabajadores.html')

@app.route('/trabajadores2/<dpi>/edit', methods=['GET', 'POST'])
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
    
@app.route('/trabajadores2/<dpi>/delete', methods=['GET', 'POST'])
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

@app.route('/trabajadores3')
def trabajores3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM trabajadores
                        ORDER BY dpi ASC""")
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

@app.route('/salones')
def salones():
    return render_template('salones.html')

@app.route('/salones2', methods=['POST'])
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
        return render_template('salones.html')

@app.route('/salones2/<id>/edit', methods=['GET', 'POST'])
def editar_salon(id):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM salon WHERE id_salon = %s", (id,))
            salon = cursor.fetchone()

        if salon:
            return render_template('editar_salon.html', salon=salon)
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
    
@app.route('/salones2/<id>/delete', methods=['GET', 'POST'])
def eliminar_salon(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM salon WHERE id_salon = %s", (id,))
                connection.commit()

            flash('El salon ha sido eliminado exitosamente.', 'success')
            return redirect('/salones3')

        return render_template('eliminar_salon.html', salon_id=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el salon.', 'error')
        return redirect('/salones3')

@app.route('/salones3')
def salones3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM salon
                        ORDER BY id_salon ASC""")
        rows = cursor.fetchall()
        return render_template('salones3.html', rows=rows)

def page_not_found(error):
    return f"<h1 style={{text-align: 'center'}}>UNDER CONSTRUCTION 🛠️</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()