from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from linguini.models import User
from linguini.database import db_session
from linguini.utils import public_route, has_role

login_manager = LoginManager()

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
@public_route
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return render_template('auth/login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        user = User.query.filter_by(username=username).first()
        if not user:
            error = 'Username does not exist.'
        if not error:
            remember_me = bool(request.form.get('remember'))
            login_user(user, remember=remember_me)
            return redirect(url_for('.index'))
        flash(error)
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
@has_role(['admin'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        pc = request.form.get('pc')
        role = request.form.get('role')
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not first_name or not last_name:
            error = 'First and last names are required.'
        elif not pc:
            error = 'A PC class is required (0 means no PC class).'
        if User.query.filter_by(username=username).first():
            error = 'Username already exists.'
        if not error:
            user = User(
                username, generate_password_hash(password), first_name, last_name, pc, role)
            db_session.add(user)
            db_session.commit()
            if current_user.is_authenticated:
                return flash('User created.')
            return redirect(url_for('.index'))
        flash(error)

    return render_template('auth/register.html')


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))


@bp.route('/', endpoint='index')
@bp.route('/login_status')
@public_route
def login_status_page():
    return render_template('auth/login_status.html')
