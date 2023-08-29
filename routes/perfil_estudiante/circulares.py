from flask import Blueprint, redirect, render_template, request, flash, url_for, send_file
from flask_login import login_required, logout_user
from database.db import get_connection

connection = get_connection()
circularesEe_bp = Blueprint('circularesEe_blueprint', __name__)

@circularesEe_bp.route('/circularesE', methods=['GET'])
@login_required
def vercircularesE():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM circulares.postsestudiantes ORDER BY creado DESC""")
        rows = cursor.fetchall()
        return render_template('estudiante/circularesE.html', rows=rows)
