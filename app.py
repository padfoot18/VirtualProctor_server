from flask import Flask, request, jsonify
import config
from flask_mysqldb import MySQL
import dialogflow_v2 as dialogflow
import os
import pprint
from functools import wraps
from flask import Flask, Response, session, flash, redirect, url_for, request, render_template, jsonify
from config import mysql_config, api_keys, flask_config
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import json

from pyfcm import FCMNotification


app = Flask(__name__)
push_service = FCMNotification(api_key=api_keys['fcm'])

# config MySQL
app.config['MYSQL_HOST'] = config.mysql_config['host']
app.config['MYSQL_USER'] = config.mysql_config['user']
app.config['MYSQL_PASSWORD'] = config.mysql_config['password']
app.config['MYSQL_DB'] = config.mysql_config['database']
app.config['MYSQL_CURSORCLASS'] = config.mysql_config['cursor_class']


# initialize MYSQL
mysql = MySQL(app)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/android_login', methods=['POST'])
def android_login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    query_result = cur.execute("SELECT * FROM users WHERE username=%s", [username])
    if query_result == 1:
        row = cur.fetchall()
        print(row)
        passwd = row[0]['password']
        role = row[0]['role']
        mysql.connection.commit()
        cur.close()
        if password == passwd:
            print(username)
            return "{\"flag\":\"true\", \"role\":"+role+"}"
        else:
            return "{\"flag\":\"password_false\", \"role\":\"None\"}"
    else:
        return "{\"flag\":\"username_false\", \"role\":\"None\"}"


@app.route('/android_chat', methods=['POST'])
def chat():
    user_query = request.form['query']
    print(request.form, user_query)

    credential_path = config.dialogflow_config['json_file']
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    project_id = config.dialogflow_config['project_id']
    session_id = "qwertyuiop"
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=user_query, language_code="en")

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    # print('Detected intent: {} (confidence: {})\n'.format(
    #     response.query_result.intent.display_name,
    #     response.query_result.intent_detection_confidence))

    matched_intent = response.query_result.intent.display_name
    print(matched_intent)

    if matched_intent == 'events':
        cur = mysql.connection.cursor()
        cur.execute("select name from event;")
        row = cur.fetchall()
        event_names = ''
        for tuples in row:
            event_names += tuples['name'] + '\n'
        resp = event_names
    elif matched_intent == 'events_description':
        print(response.query_result.parameters.fields)
        event_name = response.query_result.parameters.fields['any'].string_value
        print(event_name)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM event WHERE name = %s;", [event_name])
        row = cur.fetchall()
        description = row[0]['description']
        resp = description
    elif matched_intent == 'direct_event_description':
        print(response)
        event_name = response.query_result.parameters.fields['any'].string_value
        print(event_name)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM event WHERE name = %s;", [event_name])
        row = cur.fetchall()
        description = row[0]['description']
        resp = description
    elif matched_intent == 'subject':
        cur = mysql.connection.cursor()
        # TODO dynamic username
        cur.execute("SELECT * FROM student_personal_info WHERE username='1611032'")
        row = cur.fetchall()
        current_sem = row[0]['current_sem']
        print(current_sem)
        print(type(current_sem))
        sem = current_sem
        sem_detection = response.query_result.parameters.fields['sem_detection'].string_value
        sem_no = response.query_result.parameters.fields['sem_no'].string_value
        print(sem_detection, sem_no)
        if sem_detection != "":
            if sem_detection == 'previous':
                sem = int(current_sem) - 1
            if sem_detection == 'next':
                sem = int(current_sem) + 1
        if sem_no != "":
            sem = sem_no
        cur = mysql.connection.cursor()
        print(sem)
        # TODO dynamic username
        query = "SELECT subject FROM student_academic_info WHERE sem="+str(sem)+" and username=1611032;"
        print(query)
        cur.execute(query)
        row = cur.fetchall()
        print(row)
        subject_names = ''
        for tuples in row:
            subject_names += tuples['subject'] + '\n'
        print(subject_names)
        resp = subject_names
    elif matched_intent == 'Default Welcome Intent':
        resp = response.query_result.fulfillment_text
    elif matched_intent == 'Default Fallback Intent':
        resp = response.query_result.fulfillment_text
    else:
        resp = "Sorry, I didn't understand"
    return resp


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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """ Log in to the admin site """
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cursor = mysql.connection.cursor()
        query = 'SELECT * from users WHERE username="{}";'.format(username)
        no_of_rows = cursor.execute(query)

        if no_of_rows != 0:
            data = cursor.fetchall()[0]
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


@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin_page():
    if request.method == 'POST':
        title = request.form['notification-title']
        body = request.form['notification-body']
        print(title, body)
        result = send_notification('all', title, body)
        return render_template('admin_page.html', alert=result['success'])

    return render_template('admin_page.html')


def send_notification(to, message_title=None, message_body=None):
    # for testing
    if not message_body:
        message_body = "Hope you're having fun this weekend, don't forget to check today's news"
    if not message_title:
        message_title = 'Bhai bhai bhai bhai'

    cur = mysql.connection.cursor()
    if to == 'all':
        query = 'SELECT * from username_to_fcmId;'
    else:
        query = 'SELECT * from username_to_fcmId where username="{}";'.format(to)

    no_of_rows = cur.execute(query)
    if no_of_rows > 0:
        data = cur.fetchall()
        print(data)
        registration_ids = []
        for row in data:
            registration_ids.append(row['fcm_id'])

        # registration_ids = push_service.clean_registration_ids(registration_ids)
        print(registration_ids)

        result = push_service.notify_multiple_devices(
            registration_ids=registration_ids,
            message_title=message_title,
            message_body=message_body
        )
        print(result)
        return result
    else:
        return {'success': 0}


@app.route('/register', methods=['GET'])
def register():
    username = request.args.get('username')
    fcm_id = request.args.get('fcm_id')

    # update in the database
    # create cursor
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM username_to_fcmId WHERE username="{}";'.format(username))
    cur.execute('INSERT IGNORE INTO username_to_fcmId(username, fcm_id) VALUES("{}", "{}");'.format(username, fcm_id))
    mysql.connection.commit()
    cur.close()
    return "Update Success"


@app.route('/logout/')
@login_required
def logout():
    """ Log out from the site """
    session.clear()
    flash('You are now logged out ', 'success')
    return redirect(url_for('login'))


@app.route('/get_open_chats', methods=['GET'])
def get_open_chats():
    username = request.args.get('username')
    sql1 = 'SELECT distinct from_user from chats where to_user = "{}";'.format(username)
    sql2 = 'SELECT distinct to_user from chats where from_user = "{}";'.format(username)
    cur = mysql.connection.cursor()
    now_of_rows1 = cur.execute(sql1)
    print(sql1)
    print(sql2)
    open_chats = set()
    if now_of_rows1 > 0:
        data1 = cur.fetchall()
        print('data1', data1)
        for row in data1:
            if row['from_user'] != username:
                open_chats.add(row['from_user'])

    no_of_rows2 = cur.execute(sql2)
    if no_of_rows2 > 0:
        data2 = cur.fetchall()
        print('data2', data2)
        for row in data2:
            if row['to_user'] != username:
                open_chats.add(row['to_user'])

    open_chats = list(open_chats)
    print(open_chats)
    sql = 'SELECT username, name from users where username in ("{}");'.format('", "'.join(open_chats))
    print(sql)
    now_of_rows = cur.execute(sql)

    if now_of_rows > 0:
        data = cur.fetchall()
        print(data)

    return jsonify(data)


@app.route('/get_all_chats')
def get_all_chats():
    user1 = request.args.get('user1')
    user2 = request.args.get('user2')
    sql = '''SELECT * FROM chats where (from_user = "{}" and to_user = "{}") or (from_user = "{}" and to_user = "{}")
    order by msg_time DESC limit 10;'''.format(user1, user2, user2, user1)

    cur = mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return jsonify(data)


@app.route('/insert_chat', methods=['POST'])
def add_chat():
    temp_result = request.get_json()
    from_user = temp_result['from_user']
    print(from_user)
    to_user = temp_result['to_user']
    msg_body = temp_result['msg_body']
    password = temp_result['password']

    sql = 'SELECT * FROM users where username = "{}";'.format(from_user)
    cur = mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()[0]
    print(data)
    if data['password'] == password:
        insert_sql = 'INSERT into chats (from_user, to_user, msg_body) values ("{}", "{}", "{}");'.format(from_user,
                                                                                                          to_user,
                                                                                                          msg_body)
        print(insert_sql)
        cur.execute(insert_sql)
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True})
    # TODO(1) close cursor everywhere


if __name__ == '__main__':
    app.secret_key = flask_config['secret_key']
    app.run(debug=True)
