import config
import dialogflow_v2 as dialogflow
import os
import pprint
from functools import wraps
from flask import Flask, Response, session, flash, redirect, url_for, request, render_template, jsonify
from config import mysql_config, api_keys, flask_config
from flask_mysqldb import MySQL
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
    username = request.form['username']
    print(request.form, user_query)

    credential_path = config.dialogflow_config['json_file']
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    project_id = config.dialogflow_config['project_id']
    session_id = username
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=user_query, language_code="en")

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))

    matched_intent = response.query_result.intent.display_name
    print(matched_intent)
    print(session_id, type(session_id))
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
        event_name = response.query_result.parameters.fields['any'].string_value
        print(event_name)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM event WHERE name = %s;", [event_name])
        row = cur.fetchall()
        description = row[0]['description']
        resp = description

    elif matched_intent == 'subject':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student_personal_info WHERE username=%s", [username])
        row = cur.fetchall()
        current_sem = row[0]['current_sem']
        sem = current_sem
        sem_detection = response.query_result.parameters.fields['sem_detection'].string_value
        sem_no = response.query_result.parameters.fields['sem_no'].string_value
        if sem_detection != "":
            if sem_detection == 'previous':
                sem = int(current_sem) - 1
            if sem_detection == 'next':
                sem = int(current_sem) + 1
        if sem_no != "":
            sem = sem_no
        cur = mysql.connection.cursor()
        query = "SELECT subject FROM student_academic_info WHERE sem="+str(sem)+" and username="+username+";"
        cur.execute(query)
        row = cur.fetchall()
        subject_names = ''
        for tuples in row:
            subject_names += tuples['subject'] + '\n'
        print(subject_names)
        resp = subject_names

    elif matched_intent == 'direct_teacher':
        teacher_name = response.query_result.parameters.fields['teacher_name'].string_value.lower()
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT teacher_id, subject from student_academic_info where teacher like %s", [teacher_name])
        row = cur.fetchall()
        print(row)
        subjects = ''
        for tuples in row:
            # TODO change display statement
            subjects += tuples['teacher_id']+"\t\t⇒\t\t" + tuples['subject'] + "\n"
        resp = "Professor "+teacher_name+" teaches\n"+subjects

    elif matched_intent == 'contact_teacher':
        incoming_name = response.query_result.parameters.fields['subject'].string_value
        cur = mysql.connection.cursor()
        query = "SELECT UNIQUE teacher from student_academic_info where teacher like '" + incoming_name + "';"
        print(query)
        cur.execute(query)
        row = cur.fetchall()
        teacher_name = row[0]['teacher']

        query = "SELECT username from users WHERE teacher_name='" + teacher_name + "';"
        print(query)
        cur.execute(query)
        row = cur.fetchall()
        teacher_id = row[0]['username']
        return 'teacher' + teacher_id

    elif matched_intent == 'contact_subject_teacher':
        pass

    elif matched_intent == 'subject_to_teacher':
        subject = response.query_result.parameters.fields['subject'].string_value
        print(subject)
        cur = mysql.connection.cursor()
        query = "SELECT teacher from student_academic_info where subject='"+subject+"' and username='"+username+"';"
        print(query)
        cur.execute(query)
        row = cur.fetchall()
        print(row)
        if len(row) != 0:
            print(row[0]['teacher'])
            resp = row[0]['teacher']
        else:
            resp = "Are you sure you entered the correct subject☹️"

    elif matched_intent == 'attendance':
        params = response.query_result.parameters.fields['extremes'].string_value
        print(params)
        cur = mysql.connection.cursor()
        cur.execute("SELECT current_sem from student_personal_info where username=%s", [username])
        row = cur.fetchall()
        current_sem = row[0]['current_sem']
        if params == "":
            query = "SELECT subject, attendence from student_academic_info where username='" + username + "' and sem="+current_sem+";"
            print(query)
            cur.execute(query)
            row = cur.fetchall()
            print(row)
            attendance = ''
            for tuples in row:
                attendance += tuples['subject'] + '\t\t⇒\t\t' + tuples['attendence'] + '%\n'
            resp = attendance
        if params == "highest":
            query = "SELECT attendence from student_academic_info where username='" + username + "' and sem=" + current_sem + ";"
            print(query)
            cur.execute(query)
            row = cur.fetchall()
            max_att = []
            for tuples in row:
                max_att.append(tuples['attendence'])
            max_attendance = max(max_att)
            query = "SELECT subject from student_academic_info where username='" + username + "' and sem=" + current_sem + " and attendence="+str(max_attendance)+";"
            cur.execute(query)
            row = cur.fetchall()
            resp = "Your ward has highest attandance of " + str(max_attendance) + "% in " + row[0]['subject'] + " 😌"
        if params == "lowest":
            query = "SELECT attendence from student_academic_info where username='" + username + "' and sem=" + current_sem + ";"
            print(query)
            cur.execute(query)
            row = cur.fetchall()
            min_att = []
            for tuples in row:
                min_att.append(tuples['attendence'])
            min_attendance = min(min_att)
            query = "SELECT subject from student_academic_info where username='" + username + "' and sem=" + current_sem + " and attendence=" + str(
                min_attendance) + ";"
            cur.execute(query)
            row = cur.fetchall()
            resp = "Your child has lowest attendance of " + str(min_attendance) + " in " + row[0]['subject'] + " ☹️"
        if params == 'below_border':
            query = "SELECT subject, attendence from student_academic_info where username='" + username + "' and sem=" + current_sem + " and attendence < 75;"
            print(query)
            cur.execute(query)
            row = cur.fetchall()
            subjects = 'Your child has below par attendance in the following subjects\n'
            for tuples in row:
                subjects += tuples['subject'] + '\t\t⇒\t\t' + tuples['attendence'] + '%\n'
            resp = subjects

    elif matched_intent == 'result':
        sign_sql = 'select is_signed from digital_signature where username = "{}";'.format(username)
        print('signed_sql', sign_sql)
        cur = mysql.connection.cursor()
        num_rows = cur.execute(sign_sql)
        if num_rows > 0:
            data = cur.fetchall()[0]
            print(data)
            if data['is_signed'] == 1:
                is_signed = True
            elif data['is_signed'] == 0:
                is_signed = False


        params = response.query_result.parameters.fields['extremes'].string_value
        print(params)
        cur = mysql.connection.cursor()
        cur.execute("SELECT current_sem from student_personal_info where username=%s", [username])
        row = cur.fetchall()
        current_sem = row[0]['current_sem']
        if params == "":
            query = "SELECT subject, marks from student_academic_info where username='" + username + "' and sem=" + current_sem + ";"
            print(query)
            cur.execute(query)
            row = list(cur.fetchall())
            print(row)
            marks = 'Results of ' + username + ' for sem ' + str(current_sem) + ' \n'
            average_marks = 0
            count = 0
            for tuples in row:
                count += 1
                marks += tuples['subject'] + '\t\t⇒\t\t' + str(tuples['marks']) + '/100\n'
                average_marks += tuples['marks']
            marks += '\n' + 'Total Marks' + '\t\t⇒\t\t' + str(average_marks)
            if not is_signed:
                temp = '\n\n\nEnter your password to digitally sign the report card'
            else:
                temp = ''
            resp = marks + '\n' + 'Average Marks' + '\t\t⇒\t\t' + str(average_marks/count)+temp
        if params == "lowest":
            query = "SELECT marks from student_academic_info where username='" + username + "' and sem=" + current_sem + ";"
            print(query)
            cur.execute(query)
            row = cur.fetchall()
            min_mks = []
            for tuples in row:
                min_mks.append(tuples['marks'])
            min_marks = min(min_mks)
            query = "SELECT subject from student_academic_info where username='" + username + "' and sem=" + current_sem + " and marks="+str(min_marks)+";"
            cur.execute(query)
            row = cur.fetchall()
            resp = "Your child has got a lowest score of " + str(min_marks) + "in " + row[0]['subject'] + "😢"

        if params == 'highest':
            query = "SELECT marks from student_academic_info where username='" + username + "' and sem=" + current_sem + ";"
            print(query)
            cur.execute(query)
            row = cur.fetchall()
            max_mks = []
            for tuples in row:
                max_mks.append(tuples['marks'])
            max_marks = max(max_mks)
            query = "SELECT subject from student_academic_info where username='" + username + "' and sem=" + current_sem + " and marks=" + str(
                max_marks) + ";"
            cur.execute(query)
            row = cur.fetchall()
            resp = "Your child has got a highest score of " + str(max_marks) + "in " + row[0]['subject']

        if params == 'below_border':
            query = "SELECT subject, marks from student_academic_info where marks<40 and username='" + username + "' and sem=" + current_sem + ";"
            print(query)
            cur.execute(query)
            row = list(cur.fetchall())
            print(row)
            marks = 'Your child has failed in the following subject/n'
            for tuples in row:
                marks += tuples['subject'] + '\t\t⇒\t\t' + str(tuples['marks']) + '/100\n'
            if marks != '':
                resp = marks
            else:
                resp = "Not failed in any subject"
    elif matched_intent == 'password':
        password = int(response.query_result.parameters.fields['password'].number_value)
        print(password)
        # TODO password checking code

        sql = 'SELECT * FROM users where username = "{}";'.format(username)
        cur = mysql.connection.cursor()
        cur.execute(sql)
        data = cur.fetchall()[0]
        print(data)
        if data['password'] == str(password):
            update_sql = 'update digital_signature set is_signed = 1 where username = "{}";'.format(username)
            print(update_sql)
            cur.execute(update_sql)
            mysql.connection.commit()
            resp = 'Successfully signed the report card!'
        else:
            resp = 'Invalid password'

    elif matched_intent == 'placement':
        params = response.query_result.parameters.fields['extremes'].string_value
        print(params)
        if params == '':
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM placement")
            row = cur.fetchall()
            companies = ''
            for tuples in row:
                companies += tuples['company_name'] + "  " + str(tuples['no_student_placed']) + "  " + str(tuples['package_offered']) + '\n'
            resp = companies
        elif params == 'highest':
            cur = mysql.connection.cursor()
            cur.execute("SELECT package_offered FROM placement")
            row = cur.fetchall()
            maxi = []
            for tuples in row:
                maxi.append(tuples['package_offered'])
            max_package = max(maxi)
            cur = mysql.connection.cursor()
            query = "SELECT company_name, no_student_placed FROM placement WHERE package_offered="+str(max_package)+";"
            cur.execute(query)
            row = cur.fetchall()
            resp = 'Highest package of ' + str(max_package) + ' was offered by ' + row[0]['company_name'] + ' to ' + str(row[0]['no_student_placed']) + '  students'
        elif params == 'lowest':
            cur = mysql.connection.cursor()
            cur.execute("SELECT package_offered  FROM placement")
            row = cur.fetchall()
            mini = []
            for tuples in row:
                mini.append(tuples['package_offered'])
            min_package = min(mini)
            cur = mysql.connection.cursor()
            query = "SELECT company_name, no_student_placed FROM placement WHERE package_offered=" + str(
                min_package) + ";"
            cur.execute(query)
            row = cur.fetchall()
            resp = 'Lowest package of ' + str(min_package) + ' was offered by ' + row[0]['company_name'] + ' to ' + str(row[0]['no_student_placed']) + '  students'

    elif matched_intent == 'fees':
        pass

    elif matched_intent == "progress":
        cur = mysql.connection.cursor()
        cur.execute("SELECT current_sem from student_personal_info where username=%s", [username])
        row = cur.fetchall()
        current_sem = row[0]['current_sem']
        if int(current_sem) > 1:
            query = "SELECT SUM(marks) as marks from student_academic_info where username='" + username + "' and sem=" + current_sem + ";"
            cur.execute(query)
            row = cur.fetchall()
            total_marks_curr = row[0]['marks']
            resp = "Sem " + str(current_sem) + " total marks: " + str(total_marks_curr) + "\n"
            print(resp)
            query = "SELECT SUM(marks) as marks from student_academic_info where username='" + username + "' and sem=" + str((int(current_sem)-1)) + ";"
            cur.execute(query)
            row = cur.fetchall()
            total_marks_prev = row[0]['marks']
            resp += "Sem " + str(int(current_sem)-1) + " total marks: " + str(total_marks_prev) + "\n\n"
            print(resp)
            if total_marks_curr > total_marks_prev:
                resp += "Marks increased by " + str(total_marks_curr - total_marks_prev)
            else:
                resp += "Marks decreased by " + str(total_marks_prev - total_marks_curr)
        else:
            resp = "No data to calculate progress"

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


def send_notification(to, message_title, message_body, receiver_type='user'):
    cur = mysql.connection.cursor()
    if to == 'all':
        query = 'SELECT * from username_to_fcmId;'
    elif receiver_type == 'user':
        query = 'SELECT * from username_to_fcmId where username="{}";'.format(to)
    elif receiver_type == 'group':
        query = 'SELECT * FROM username_to_fcmId natural join user_to_group where group_id = "{}";'.format(to)
        print(query)
        # TODO complete this query!!! wrong query!!!

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
    sql = '''SELECT * FROM chats where (from_user = "{}" and to_user = "{}") or (from_user = "{}" and to_user = "{}");'''.format(user1, user2, user2, user1)

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
        send_notification(to_user, 'New message', msg_body, 'user')
        cur.close()
        return jsonify({'success': True})
    # TODO(1) close cursor everywhere


@app.route('/get_groups', methods=['GET'])
def get_groups():
    sql = 'SELECT * from groups;'
    cur = mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    return jsonify(data)


@app.route('/broadcast_to_group', methods=['POST'])
def broadcast_msg():
    form_data = request.get_json()
    from_user = form_data['from_user']
    password = form_data['password']
    group_id = form_data['group_id']
    message = form_data['msg_body']

    sql = 'SELECT * FROM users where username = "{}";'.format(from_user)
    cur = mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()[0]
    print(data)
    if data['password'] == password:
        insert_sql = 'INSERT INTO broadcast_msg (from_id, group_id, msg_body) values ("{}", "{}", "{}");'.format(
            from_user, group_id, message)
        print(insert_sql)
        cur = mysql.connection.cursor()
        cur.execute(insert_sql)
        mysql.connection.commit()
        # TODO send notification
        send_notification(group_id, 'New broadcast message', message, 'group')
        return jsonify({'success': 1})


@app.route('/get_broadcast_msg', methods=['GET'])
def get_broadcast_msg():
    username = request.args.get('username')
    sql = '''SELECT group_id, msg_body, msg_time, name FROM broadcast_msg natural join groups join users on from_id = username where group_id in (
    SELECT group_id from user_to_group where username = "{}") order by msg_time desc limit 10;'''.format(username)
    print(sql)

    cur = mysql.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    return jsonify(data)


if __name__ == '__main__':
    app.secret_key = flask_config['secret_key']
    app.run(debug=True)
