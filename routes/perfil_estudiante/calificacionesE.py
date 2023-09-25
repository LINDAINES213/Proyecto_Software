from flask import Blueprint, redirect, render_template, request, flash, redirect
from flask_login import login_required, login_user
from database.db import get_connection
from models.ModelUser import ModelUser
from models.entities.User import User
from models.entities.UserS import UserS

connection = get_connection()
calificacionesE_bp = Blueprint('calificacionesE_blueprint', __name__)

@calificacionesE_bp.route('/formcalificacionesE')
@login_required
def verCalificaciones():
    return render_template('estudiante/formcalificacionesE.html')

@calificacionesE_bp.route('/formcalificacionesE', methods=['POST'])
@login_required
def verificarCalificaciones():
    if request.method == 'POST':
        id_estudiante = request.form['id_estudiante']
        contrasena = request.form['contrasena']
        user = UserS(0, id_estudiante, contrasena)
        logged_user = ModelUser.loginE(connection, user)
        if logged_user != None:
            if logged_user.contrasena:
                login_user(logged_user)
                return redirect(f'/calificacionesE/{id_estudiante}')
            else:
                flash("ID o contraseña incorrecto...")
                return redirect('/formcalificacionesE')
        else:
                flash("ID o contraseña incorrecto......")
                return redirect('/formcalificacionesE')
    else:
        return redirect('/formcalificacionesE')

@calificacionesE_bp.route('/calificacionesE')
@login_required
def calificacionesE():
    return render_template('estudiante/calificacionesE.html')


@calificacionesE_bp.route('/calificacionesE/<string:id_estudiante>')
@login_required
def calificacion(id_estudiante):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM calificaciones
                        WHERE id_estudiante = %s""",(id_estudiante,))
        rows = cursor.fetchall()
        return render_template('estudiante/calificacionesE.html', rows=rows)