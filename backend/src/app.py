from flask import Flask, render_template, request, redirect, url_for
from database.db import get_connection
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from flask_cors import CORS
from config import config


app = Flask(__name__)
csrf = CSRFProtect(app)
connection = get_connection()
CORS(app)

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
        id_medico = request.form['id_medico']
        dpi = request.form['dpi']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        num_colegiado = request.form['num_colegiado']
        especialidades = request.form['especialidades']
        hospital = request.form['hospital']
        fecha_contratacion = request.form['fecha_contratacion']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO medicos VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (id_medico, dpi, nombre, telefono, direccion, num_colegiado, especialidades, hospital, fecha_contratacion, correo, contrasena))
            connection.commit()                
        cursor.close()
        return render_template('confirmaciones.html',)

    except Exception as ex:
        return render_template('usuarios.html')


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