from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required
from database.db import get_connection


connection = get_connection()
colegiatura_bp = Blueprint('colegiatura_blueprint', __name__)

@colegiatura_bp.route('/pagoC')
@login_required
def pagoC():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM estudiantes
                        ORDER BY grado ASC""")
        rows = cursor.fetchall()
        return render_template('admin/pagoC.html', rows=rows)
