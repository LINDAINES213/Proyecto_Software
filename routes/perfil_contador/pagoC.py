from flask import Blueprint, redirect, render_template, request, flash, redirect
from flask_login import login_required, login_user
from database.db import get_connection
from models.ModelUser import ModelUser
from models.entities.User import User
from models.entities.UserS import UserS

connection = get_connection()
colegiatura_bp = Blueprint('colegiatura_blueprint', __name__)

@colegiatura_bp.route('/formcolegiaturas')
@login_required
def formcolegiaturas():
    return render_template('admin/formcolegiaturas.html')

def get_id_from_database(id_estudiante):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id_estudiante FROM usuarios.userestudiantes
                                WHERE id_estudiante = %s""", (id_estudiante,))
            row = cursor.fetchone()
           
            if row:
                id_estudiante = row[0]
                return id_estudiante
            else:
                return id_estudiante

    except Exception as ex:
        print(f"Error al obtener el cargo del usuario: {ex}")
        return None

@colegiatura_bp.route('/formcolegiaturas', methods=['POST'])
@login_required
def verificarPagoC():
    if request.method == 'POST':
        id_estudiante = request.form['id_estudiante']
        contrasena = request.form['contrasena']
        id2 = get_id_from_database(id)
        user = UserS(0, id_estudiante, contrasena)
        logged_user = ModelUser.loginE(connection, user)
        if logged_user != None:
            if logged_user.id_estudiante:
                login_user(logged_user)
                if logged_user.id_estudiante == id_estudiante:
                    return redirect(f'/pagoC/{id_estudiante}')
            else:
                flash("ID incorrecto...")
                return redirect('/formcolegiaturas')
        else:
                flash("ID incorrecto......")
                return redirect('/formcolegiaturas')
    else:
        return redirect('/formcolegiaturas')

@colegiatura_bp.route('/pagoC')
@login_required
def pagosC():
    return render_template('admin/pagoC.html')


@colegiatura_bp.route('/pagoC/<string:id_estudiante>')
@login_required
def pagoC(id_estudiante):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM estudiantes
                        WHERE id_estudiante = %s""",(id_estudiante,))
        rows = cursor.fetchall()
        return render_template('admin/pagoC.html', rows=rows)
