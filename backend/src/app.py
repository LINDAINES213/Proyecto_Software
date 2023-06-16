from flask import Flask, render_template, request, redirect, flash, url_for, send_file
from database.db import get_connection
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_cors import CORS
from config import config
from dotenv import load_dotenv

################## Funcionalidades para Coordinador ###################
from models.entities.User import User
from models.ModelUser import ModelUser
from routes.perfil_trabajador.trabajadores import trabajadores_bp
from routes.perfil_trabajador.estudiantes import estudiantes_bp
from routes.perfil_trabajador.maestros import maestros_bp
from routes.perfil_trabajador.cursos import cursos_bp
from routes.perfil_trabajador.salones import salones_bp
from routes.perfil_trabajador.grados import grados_bp
from routes.perfil_trabajador.secciones import secciones_bp
from routes.perfil_trabajador.pagos import pagos_bp
from routes.perfil_trabajador.crearUsuario import crearUsuario_bp
#######################################################################

################## Funcionalidades para Maestro ###################

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect(app)
connection = get_connection()
login_manager_app = LoginManager(app)
CORS(app)

###### Funcionalidades para Coordinador ######
app.register_blueprint(trabajadores_bp)
app.register_blueprint(estudiantes_bp)
app.register_blueprint(maestros_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(salones_bp)
app.register_blueprint(grados_bp)
app.register_blueprint(secciones_bp)
app.register_blueprint(pagos_bp)
app.register_blueprint(crearUsuario_bp)
#############################################


##################### INICIOS PERFILES #####################
@app.route('/')
def inicio():
    return render_template('home.html')

@app.route('/inicioadmin')
@login_required
def inicioadmin():
    return render_template('inicioadmin.html')

@app.route('/iniciocontador')
@login_required
def iniciocontador():
    return render_template('iniciocontador.html')

@app.route('/iniciodirector')
@login_required
def iniciodirector():
    return render_template('iniciodirector.html')

@app.route('/iniciosecretario')
@login_required
def iniciosecretario():
    return render_template('iniciosecretario.html')

@app.route('/iniciomaestro')
@login_required
def iniciomaestro():
    return render_template('iniciomaestro.html')

############################# LOGIN ##############################
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(connection, id)

def get_cargo_from_database(dpi):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT cargo FROM usuarios.user
                                WHERE dpi = %s""", (dpi,))
            row = cursor.fetchone()
           
            if row:
                cargo = row[3]
                return cargo
            else:
                return None

    except Exception as ex:
        print(f"Error al obtener el cargo del usuario: {ex}")
        return None

@app.route('/logint', methods=['GET', 'POST'])
def logint():
    if request.method == 'POST':
        dpi = request.form['dpi']
        contrasena = request.form['contrasena']
        cargo = get_cargo_from_database(dpi)
        user = User(0, dpi, contrasena)
        logged_user = ModelUser.login(connection, user)
        if logged_user != None:
            if logged_user.contrasena:
                login_user(logged_user)
                if logged_user.cargo == "Maestro":
                    return redirect(url_for('iniciomaestro'))
                elif logged_user.cargo == "Coordinador":
                    return redirect(url_for('inicioadmin'))
                elif logged_user.cargo == "Director":
                    return redirect(url_for('iniciodirector'))
                elif logged_user.cargo == "Secretario":
                    return redirect(url_for('iniciosecretario'))
                elif logged_user.cargo == "Contador":
                    return redirect(url_for('iniciocontador'))
            else:
                flash("Invalid password...")
                return render_template('loginT.html')
        else:
            flash("Contrasena o usuario incorrectos...")
            return render_template('loginT.html')
    else:
        return render_template('loginT.html')
    
################ LOGOUT ################
@app.route('/logoutt')
@login_required
def logoutt():
    logout_user()
    return redirect(url_for('logint'))

################################# EJECUCION API #######################################
def page_not_found(error):
    return f"<h1 style='min-height: 700px;display: flex;align-items: center;justify-content: center;'>UNDER CONSTRUCTION 🛠️</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()
########################################################################################