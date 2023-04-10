from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@login_required
@app.route('/dashboard')
def dashboard():
    links = current_user.links
    return render_template('dashboard.html', links=links)

@login_required
@app.route('/add-link', methods=['POST'])
def add_link():
    url = request.form.get('url')
    if url:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        link = Link(url=url, short_code=short_code, user_id=current_user.id)
        try:
            db.session.add(link)
            db.session.commit()
            flash('Link added successfully', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Link already exists', 'danger')
    else:
        flash('Please enter a URL', 'danger')
    return redirect(url_for('dashboard'))
