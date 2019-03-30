import pprint
from functools import wraps
from flask import Flask, Response, session, flash, redirect, url_for, request, render_template, jsonify
from config import mysql_config, api_keys
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

from pyfcm import FCMNotification


app = Flask(__name__)

# mysql configuration
app.config['MYSQL_HOST'] = mysql_config['host']
app.config['MYSQL_USER'] = mysql_config['user']
app.config['MYSQL_PASSWORD'] = mysql_config['password']
app.config['MYSQL_DB'] = mysql_config['database']
app.config['MYSQL_CURSORCLASS'] = mysql_config['cursor_class']

mysql = MySQL(app)
push_service = FCMNotification(api_key=api_keys['fcm'])


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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """ Log in to the admin site """
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cursor = mysql.connection.cursor()
        query = 'SELECT * from users WHERE username="{}"'.format(username)
        no_of_rows = cursor.execute(query)

        if no_of_rows != 0:
            data = cursor.fetchall()
            pprint.pprint(data)

            password = data['password']
            role = data['role']
            # if sha256_crypt.verify(password_candidate, password) and role == 'admin':
            if password_candidate == password and role == 'admin':
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect('/admin/')

            else:
                app.logger.info('PASSWORD NOT MATCHED')
                error = 'Incorrect Password'
                return render_template('login.html', error=error)

        else:
            app.logger.info('NO USER')
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


@login_required
@app.route('/admin/', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        title = request.form['notification-title']
        body = request.form['notification-body']
        result = send_notification('all', title, body)
        return render_template('admin_page.html', alert=result['success'])

    return render_template('admin_page.html')


def send_notification(to, message_title=None, message_body=None):
    # for testing
    if not message_body:
        message_body = "Hope you're having fun this weekend, don't forget to check today's news"
    if not message_title:
        message_title = 'Bhai bhai bhai bhai'

    if to == 'all':
        cur = mysql.connection.cursor()
        query = 'SELECT * from registration_ids;'
        no_of_rows = cur.execute(query)

        if no_of_rows > 0:
            data = cur.fetchall()
            registration_ids = []
            for row in data:
                registration_ids.append(data['registration_id'])

            registration_ids = push_service.clean_registration_ids(registration_ids)

            result = push_service.notify_multiple_devices(
                registration_ids=registration_ids,
                message_title=message_title,
                message_body=message_body
            )

            return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
