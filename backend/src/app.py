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

"""class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Event: {self.description}"
    
    def __init__(self, description):
        self.description = description"""



@app.route('/')
def hello():
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



@app.route('/maestros')
def maestros():
    return render_template('maestros.html')

@app.route('/trabajadores3')
def trabajores3():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM trabajador
                        ORDER BY id_trabajador ASC""")
        rows = cursor.fetchall()
        return render_template('trabajores3.html', rows=rows)

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

#create events
@app.route('/events', methods=['POST'])
def create_event():
    description = request.json['description']
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

#get all events
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.order_by(Event.created_at.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {'events': event_list}

#get single event
@app.route('/events/<id>', methods=['GET'])
def get_event(id):
    try:
        event = Event.query.filter_by(id=id).one()
    except NoResultFound:
        return {'error': 'Event not found'}
    
    formatted_event = format_event(event)
    return {'event': formatted_event}

#delete an event
@app.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
     event = Event.query.filter_by(id=id).one()
     db.session.delete(event)
     db.session.commit()
     return f'Event (id: {id}) deleted!'

#edit an event
@app.route('/events/<id>', methods=['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id)
    description = request.json['description']
    event.update(dict(description = description, created_at = datetime.utcnow()))
    db.session.commit()
    return {'event': format_event(event.one())}

def page_not_found(error):
    return "<h1>Not found page</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()