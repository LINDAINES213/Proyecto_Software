from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, logout_user
from src.database.db import get_connection


connection = get_connection()
logOut_bp = Blueprint('logOut_blueprint', __name__)

