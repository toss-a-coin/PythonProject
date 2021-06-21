from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute(
        'select t.id, t.description, u.username, t.completed, t.created_at from todo t JOIN user u on t.created_by = u.id order by created_at desc '
    )

    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        description = request.form['Descripcion']
        error = None

        if not description:
            error = 'La descripcion es requerida'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()

            c.execute(
                'insert into todo (description, completed, created_by)'
                ' values (%s, %s, %s)',
                (description, False, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update():
    return render_template('todo/update.html', todo=todo)
