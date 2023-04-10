from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .forms import LoginForm, RegistrationForm
from .utils import login_required


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user."""
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        db = get_db()
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        error = None

        if db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            error = f"User {username} is already registered."
        elif db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone() is not None:
            error = f"Email {email} is already registered."

        if error is None:
            db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (username, email, password))
            db.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    """Log in the user."""
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        db = get_db()
        username = form.username.data
        password = form.password.data
        error = None
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'Invalid username or password.'
        elif not check_password_hash(user['password'], password):
            error = 'Invalid username or password.'

        if error is None:
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
