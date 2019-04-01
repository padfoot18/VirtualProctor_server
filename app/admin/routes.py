from flask import session, redirect, flash, url_for, request, render_template
from functools import wraps
from app.push_notification.notifications import send_notification
from app.admin import admin_bp
from app import db


def login_required(f):
    """
    decorator to check if user is logged in
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
def admin_page():
    if request.method == 'POST':
        title = request.form['notification-title']
        body = request.form['notification-body']
        print(title, body)
        result = send_notification('all', title, body)
        return render_template('admin_page.html', alert=result['success'])

    return render_template('admin_page.html')


@admin_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """ Log in to the admin site """
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cursor = db.connection.cursor()
        query = 'SELECT * from users WHERE username="{}";'.format(username)
        no_of_rows = cursor.execute(query)

        if no_of_rows != 0:
            data = cursor.fetchall()[0]

            password = data['password']
            role = data['role']
            # if sha256_crypt.verify(password_candidate, password) and role == 'admin':
            if password_candidate == password and role == 'admin':
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect('/admin/')

            else:
                error = 'Incorrect Password'
                return render_template('login.html', error=error)

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')
