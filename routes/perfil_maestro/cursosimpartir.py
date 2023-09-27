from flask import Blueprint, redirect, render_template, request, flash, redirect
from flask_login import login_required, login_user
from database.db import get_connection
from models.ModelUser import ModelUser
from models.entities.User import User
from models.entities.UserS import UserS

connection = get_connection()
cursosimpartir_bp = Blueprint('cursosimpartir_blueprint', __name__)

@cursosimpartir_bp.route('/cursosI')
@login_required
def cursosimpartir():
    return render_template('maestro/cursosimpartir.html')

#user = User(0, dpi)
#logged_user = ModelUser.login(connection, user)

def get_dpi_from_database(dpi):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT dpi FROM usuarios.user
                                WHERE dpi = %s and cargo = 'Maestro'""", (dpi,))
            row = cursor.fetchone()
           
            if row:
                dpi = row[0]
                return dpi
            else:
                return dpi

    except Exception as ex:
        print(f"Error al obtener el cargo del usuario: {ex}")
        return None

@cursosimpartir_bp.route('/cursosI', methods=['POST'])
@login_required
def verificarCursosAImpartir():
    if request.method == 'POST':
        dpi = request.form['dpi']
        contrasena = request.form['contrasena']
        dpi2 = get_dpi_from_database(dpi)
        user = User(0, dpi, contrasena)
        logged_user = ModelUser.login(connection, user)
        if logged_user != None:
            if logged_user.dpi:
                login_user(logged_user)
                if logged_user.dpi == dpi:
                    return redirect(f'/cursosImpartir/{dpi}')
            else:
                flash("DPI incorrecto...")
                return redirect('/cursosI')
        else:
                flash("DPI incorrecto......")
                return redirect('/cursosI')
    else:
        return redirect('/cursosI')

@cursosimpartir_bp.route('/cursosImpartir')
@login_required
def salarios():
    return render_template('maestro/cursosimpartir2.html')


@cursosimpartir_bp.route('/cursosImpartir/<string:dpi>')
@login_required
def salario(dpi):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT curso.id_curso, curso.curso, maestros.dpi, maestros.nombre, curso.hora_inicio, curso.hora_fin FROM curso JOIN maestros on curso.maestro = maestros.dpi
                       WHERE maestros.dpi = %s""",(dpi,))
        rows = cursor.fetchall()
        return render_template('maestro/cursosimpartir2.html', rows=rows)
