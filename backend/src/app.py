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
        fecha_pago = request.form['fecha_pago']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO trabajadores VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (dpi, nombres, apellidos, cargo, salario, metodo_de_pago, bonus, fecha_contratacion, fecha_pago))
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
    
@app.route('/estudiantes')
def estudiantes():
    return render_template('estudiantes.html')

@app.route('/estudiantes2', methods=['POST'])
def estudiantes2():
    try:
        id_estudiante = request.form['id_estudiante']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        edad = request.form['edad']
        grado = request.form['grado']
        seccion = request.form['seccion']
        curso1 = request.form['curso1']
        curso2 = request.form['curso2']
        curso3 = request.form['curso3']
        curso4 = request.form['curso4']
        curso5 = request.form['curso5']
        curso6 = request.form['curso6']
        curso7 = request.form['curso7']
        curso8 = request.form['curso8']
        curso9 = request.form['curso9']
        curso10 = request.form['curso10']
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO estudiantes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (id_estudiante, nombres, apellidos, fecha_nacimiento, edad, grado, seccion, curso1, curso2, curso3, curso4, curso5, curso6, curso7, curso8, curso9, curso10))
            connection.commit()  
        return redirect('/estudiantes3')
    except Exception as ex:
        return render_template('estudiantes.html')
    
@app.route('/estudiantes2/<id>/edit', methods=['GET', 'POST'])
def editar_estudiante(id):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM estudiantes WHERE id_estudiante = %s", (id,))
            estudiante = cursor.fetchone()

        if estudiante:
            return render_template('editar_estudiante.html', estudiante=estudiante)
        else:
            return 'Estudiante no encontrado'

    elif request.method == 'POST':
        # Actualizar los datos del trabajador en la base de datos
        id_estudiante = request.form['id_estudiante']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        edad = request.form['edad']
        grado = request.form['grado']
        seccion = request.form['seccion']
        curso1 = request.form['curso1']
        curso2 = request.form['curso2']
        curso3 = request.form['curso3']
        curso4 = request.form['curso4']
        curso5 = request.form['curso5']
        curso6 = request.form['curso6']
        curso7 = request.form['curso7']
        curso8 = request.form['curso8']
        curso9 = request.form['curso9']
        curso10 = request.form['curso10']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE estudiantes SET
                nombres = %s,
                apellidos = %s,
                fecha_nacimiento = %s,
                edad =%s,
                grado = %s,
                seccion = %s,
                curso1 = %s,
                curso2 = %s,
                curso3 = %s,
                curso4 = %s, 
                curso5 = %s,
                curso6 = %s,
                curso7 = %s,
                curso8 = %s,
                curso9 = %s,
                curso10 = %s
                WHERE id_estudiante = %s
            """, (nombres, apellidos, fecha_nacimiento, edad, grado, seccion, curso1, curso2, curso3, curso4, curso5, curso6, curso7, curso8, curso9, curso10, id_estudiante))
            connection.commit()

        return redirect('/estudiantes3')
    
@app.route('/estudiantes2/<id>/delete', methods=['GET', 'POST'])
def eliminar_estudiante(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM estudiantes WHERE id_estudiante = %s", (id,))
                connection.commit()

            flash('El Estudiante ha sido eliminado exitosamente.', 'success')
            return redirect('/estudiantes3')

        return render_template('eliminar_estudiante.html', id_estudiante=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el trabajador.', 'error')
        return redirect('/estudiantes3')

@app.route('/estudiantes3')
def estudiantes3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM estudiantes
                        ORDER BY id_estudiante ASC""")
        rows = cursor.fetchall()
        return render_template('estudiantes3.html', rows=rows)

@app.route('/maestros')
def maestros():
    return render_template('maestros.html')

@app.route('/maestros2', methods=['POST'])
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

@app.route('/maestros2/<dpi>/edit', methods=['GET', 'POST'])
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
    
@app.route('/maestros2/<dpi>/delete', methods=['GET', 'POST'])
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

@app.route('/maestros3')
def mestros3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT t.dpi, CONCAT(t.nombres,' ', t.apellidos) AS maestro, curso_1, curso_2 FROM maestros
                        LEFT JOIN trabajadores t ON t.dpi = maestros.dpi
                        ORDER BY dpi ASC""")
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
        cursor.execute("""SELECT id_curso, nombre, CONCAT(t.nombres,' ', t.apellidos) AS maestro, salon, hora_inicio, hora_fin FROM curso
                        LEFT JOIN trabajadores t ON t.dpi = curso.maestro
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
    
@app.route('/grados')
def grados():
    return render_template('grados.html')

@app.route('/grados2', methods=['POST'])
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
        return render_template('grados.html')

@app.route('/grados2/<id>/edit', methods=['GET', 'POST'])
def editar_grado(id):
    if request.method == 'GET':
        # Obtener los datos del trabajador por su ID y mostrar el formulario de edición
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM grado WHERE id_grado = %s", (id,))
            grado = cursor.fetchone()

        if grado:
            return render_template('editar_grado.html', grado=grado)
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
    
@app.route('/grados2/<id>/delete', methods=['GET', 'POST'])
def eliminar_grado(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM grado WHERE id_grado = %s", (id,))
                connection.commit()

            flash('El salon ha sido eliminado exitosamente.', 'success')
            return redirect('/grados3')

        return render_template('eliminar_grado.html', id_grado=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el salon.', 'error')
        return redirect('/grados3')

@app.route('/grados3')
def grados3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM grado
                        ORDER BY id_grado ASC""")
        rows = cursor.fetchall()
        return render_template('grados3.html', rows=rows)
    
@app.route('/secciones')
def secciones():
    return render_template('secciones.html')

@app.route('/secciones2', methods=['POST'])
def secciones2():
    try:
        id_seccion = request.form['id_seccion']
        id_grado = request.form['id_grado']
        seccion = request.form['seccion']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO seccion VALUES (%s, %s, %s)""", 
                           (id_seccion, id_grado, seccion))
            connection.commit()  
        return redirect('/secciones3')
    except Exception as ex:
        return render_template('secciones.html')

@app.route('/secciones2/<id>/edit', methods=['GET', 'POST'])
def editar_seccion(id):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM seccion WHERE id_seccion = %s", (id,))
            seccion = cursor.fetchone()

        if seccion:
            return render_template('editar_seccion.html', seccion=seccion)
        else:
            return 'Seccion no encontrado'

    elif request.method == 'POST':
        id_seccion = request.form['id_seccion']
        seccion = request.form['seccion']

        with connection.cursor() as cursor:
            cursor.execute("""UPDATE seccion SET
                seccion = %s
                WHERE id_seccion = %s
            """, (seccion, id_seccion))
            connection.commit()

        return redirect('/secciones3')
    
@app.route('/secciones2/<id>/delete', methods=['GET', 'POST'])
def eliminar_seccion(id):
    try:
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM seccion WHERE id_seccion = %s", (id,))
                connection.commit()

            flash('El salon ha sido eliminado exitosamente.', 'success')
            return redirect('/secciones3')

        return render_template('eliminar_seccion.html', id_seccion=id)

    except Exception as ex:
        flash('Ocurrió un error al intentar eliminar el salon.', 'error')
        return redirect('/secciones3')

@app.route('/secciones3')
def secciones3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM seccion
                        ORDER BY id_seccion ASC""")
        rows = cursor.fetchall()
        return render_template('secciones3.html', rows=rows)

@app.route('/pagoP')
def pagoP():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM trabajadores
                        ORDER BY dpi ASC""")
        rows = cursor.fetchall()
        return render_template('pagoP.html', rows=rows)
    
@app.route('/pagoC')
def pagoC():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM estudiantes
                        ORDER BY id_estudiante ASC""")
        rows = cursor.fetchall()
        return render_template('pagoC.html', rows=rows)

def page_not_found(error):
    return f"<h1 style={{text-align: 'center'}}>UNDER CONSTRUCTION 🛠️</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()