import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        password_hash = generate_password_hash(password)
        # password_hash = generate_password_hash(password)
        db, c = get_db()
        error = None

        c.execute(
            'select id from user where username = %s', (username,)
        )

        if not username:
            error = 'Username is required'

        if not password:
            error = 'Password is required'
        elif c.fetchone() is not None:
            error = 'Username {} is already registered'.format(username)
        if error is None:
            c.execute(
                'insert into user (username, password) values (%s, %s)',
                (username, password_hash)
            )
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']

        db, c = get_db()
        error = None

        c.execute(
        'select * from user where username = %s', (username,)
        )
        user = c.fetchone()

        # # if user is None:
        # #     error = 'Username and/or incorrect'
        # if user is None:
        #     error = None
        # # elif not check_password_hash(user['password'], password):
        # #     error = 'Username and/or incorrect'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect (url_for('todo.index'))

        flash (error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
