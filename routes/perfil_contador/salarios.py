from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required, login_user
from database.db import get_connection
from models.ModelUser import ModelUser
from models.entities.User import User
from models.entities.UserS import UserS

connection = get_connection()
salarios_bp = Blueprint('salarios_blueprint', __name__)

@salarios_bp.route('/formsalarios')
@login_required
def formsalarios():
    return render_template('admin/formsalarios.html')

#user = User(0, dpi)
#logged_user = ModelUser.login(connection, user)

def get_dpi_from_database(dpi):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT dpi FROM usuarios.user
                                WHERE dpi = %s""", (dpi,))
            row = cursor.fetchone()
           
            if row:
                dpi = row[0]
                return dpi
            else:
                return dpi

    except Exception as ex:
        print(f"Error al obtener el cargo del usuario: {ex}")
        return None

@salarios_bp.route('/formsalarios', methods=['POST'])
@login_required
def verificarSalario():
    if request.method == 'POST':
        dpi = request.form['dpi']
        dpi2 = get_dpi_from_database(dpi)
        user = User(0, dpi)
        logged_user = ModelUser.login(connection, user)
        if logged_user != None:
            if logged_user.dpi:
                login_user(logged_user)
                if logged_user.dpi2 == dpi:
                    salario()
            else:
                flash("DPI incorrecto...")
                return redirect('/formsalarios')
        else:
                flash("DPI incorrecto......")
                return redirect('/formsalarios')
    else:
        return redirect('/formsalarios')

@salarios_bp.route('/salario')
@login_required
def salarios():
    return render_template('admin/salarios.html')


@salarios_bp.route('/salario')
@login_required
def salario(dpi):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM trabajadores
                        WHERE dpi = %s""",(dpi))
        rows = cursor.fetchall()
        return render_template('admin/salarios.html', rows=rows)
