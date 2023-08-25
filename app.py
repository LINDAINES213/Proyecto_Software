from flask import Flask, render_template, request, redirect, flash, url_for, Response, session
from src.database.db import get_connection
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_cors import CORS
from src.config import config
from dotenv import load_dotenv
from flask import Response

################## Funcionalidades para Coordinador ###################
from src.models.entities.User import User
from src.models.entities.UserS import UserS
from src.models.ModelUser import ModelUser
from src.routes.perfil_admin.trabajadores import trabajadores_bp
from src.routes.perfil_admin.estudiantes import estudiantes_bp
from src.routes.perfil_admin.maestros import maestros_bp
from src.routes.perfil_admin.cursos import cursos_bp
from src.routes.perfil_admin.salones import salones_bp
from src.routes.perfil_admin.grados import grados_bp
from src.routes.perfil_admin.secciones import secciones_bp
from src.routes.perfil_admin.pagos import pagos_bp
from src.routes.perfil_admin.crearUsuario import crearUsuario_bp
from src.routes.perfil_admin.crearEstudiante import crearEstudiante_bp 
#######################################################################

################## Funcionalidades para Director ###################
from src.routes.perfil_director.pagos_director import pagosdirector_bp
from src.routes.perfil_director.calificaciones import calificaciones_bp
#######################################################################

################## Funcionalidades para Secretario ###################
from src.routes.perfil_secretario.circularesT import circularesT_bp
from src.routes.perfil_secretario.circularesE import circularesE_bp
#######################################################################

################## Funcionalidades para Maestro ###################
#######################################################################

################## Funcionalidades para Contador ###################
#######################################################################

################## Funcionalidades para Estudiantes/Padres de Familia ###################
#######################################################################

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'SOFTWARE_123'
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
app.register_blueprint(crearEstudiante_bp)
#############################################

###### Funcionalidades para Director ######
app.register_blueprint(pagosdirector_bp)
app.register_blueprint(calificaciones_bp)
#############################################

###### Funcionalidades para Secretario ######
app.register_blueprint(circularesT_bp)
app.register_blueprint(circularesE_bp)
#############################################

###### Funcionalidades para Maestro ######
#############################################

###### Funcionalidades para Contador ######
#############################################

###### Funcionalidades para Estudiante/Padres de Familia ######
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

@app.route('/inicioestudiante')
@login_required
def inicioestudiante():
    return render_template('inicioestudiante.html')

############################# LOGIN ##############################
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_idE(connection, id) or ModelUser.get_by_id(connection, id) 

def get_cargo_from_database(dpi):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT cargo FROM usuarios.user
                                WHERE dpi = %s""", (dpi,))
            row = cursor.fetchone()
           
            if row:
                cargo = row[0]
                return cargo
            else:
                return cargo

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
                flash("DPI o contraseña incorrecta...")
                return render_template('auth/Trabajadores/loginT.html')
        else:
                flash("DPI o contraseña incorrecta......")
                return render_template('auth/Trabajadores/loginT.html')
    
    else:
        return render_template('auth/Trabajadores/loginT.html')
    


    
@app.route('/logine', methods=['GET', 'POST'])
def logine():
    if request.method == 'POST':
        id_estudiante = request.form['id_estudiante']
        contrasena = request.form['contrasena']
        user = UserS(0, id_estudiante, contrasena)
        logged_user = ModelUser.loginE(connection, user)
        if logged_user != None:
            if logged_user.contrasena:
                login_user(logged_user)
                return redirect(url_for('inicioestudiante'))
            else:
                flash("DPI o contraseña incorrecta...")
                return render_template('auth/Estudiantes/loginE.html')
        else:
                flash("DPI o contraseña incorrecta......")
                return render_template('auth/Estudiantes/loginE.html')
    
    else:
        return render_template('auth/Estudiantes/loginE.html')
    
################ LOGOUT ################
@app.route('/logoutt')
@login_required
def logoutt():
    logout_user()
    return redirect(url_for('inicio'))

################################# EJECUCION API #######################################
def page_not_found(error):
    return f"<h1 style='min-height: 700px;display: flex;align-items: center;justify-content: center;'>UNDER CONSTRUCTION 🛠️</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()
########################################################################################