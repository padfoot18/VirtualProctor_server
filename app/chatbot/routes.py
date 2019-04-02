from flask import request
from app import db
import personal_config
import os
import dialogflow_v2 as dialogflow
from app.chatbot import chatbot_bp


# TODO: return json response everywhere
@chatbot_bp.route('/login', methods=['POST'])
def android_login():
    username = request.form['username']
    password = request.form['password']

    cur = db.connection.cursor()
    query_result = cur.execute("SELECT * FROM users WHERE username=%s", [username])
    if query_result == 1:
        row = cur.fetchall()
        print(row)
        passwd = row[0]['password']
        role = row[0]['role']
        db.connection.commit()
        cur.close()
        if password == passwd:
            print(username)
            return "{\"flag\":\"true\", \"role\":"+role+"}"
        else:
            return "{\"flag\":\"password_false\", \"role\":\"None\"}"
    else:
        return "{\"flag\":\"username_false\", \"role\":\"None\"}"


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    user_query = request.form['query']
    username = request.form['username']
    print(request.form, user_query)

    credential_path = personal_config.dialogflow_config['json_file']
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    project_id = personal_config.dialogflow_config['project_id']
    session_id = username
    session_client = dialogflow.SessionsClient()

    dialogflow_session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=user_query, language_code="en")

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=dialogflow_session, query_input=query_input)
    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))

    matched_intent = response.query_result.intent.display_name
    print(matched_intent)
    print(session_id, type(session_id))
    if matched_intent == 'events':
        cur = db.connection.cursor()
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
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM event WHERE name = %s;", [event_name])
        row = cur.fetchall()
        description = row[0]['description']
        resp = description

    elif matched_intent == 'direct_event_description':
        event_name = response.query_result.parameters.fields['any'].string_value
        print(event_name)
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM event WHERE name = %s;", [event_name])
        row = cur.fetchall()
        description = row[0]['description']
        resp = description

    elif matched_intent == 'subject':
        cur = db.connection.cursor()
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
        cur = db.connection.cursor()
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
        cur = db.connection.cursor()
        cur.execute('SELECT DISTINCT teacher_id, subject from student_academic_info where teacher like "{}%"'.format(teacher_name))
        row = cur.fetchall()
        print(row)
        subjects = ''
        for tuples in row:
            subjects += tuples['teacher_id']+"\t\t⇒\t\t" + tuples['subject'] + "\n"
        resp = "Professor "+teacher_name+" teaches\n"+subjects

    elif matched_intent == 'contact_teacher':
        incoming_name = response.query_result.parameters.fields['teacher_name'].string_value
        cur = db.connection.cursor()
        query = "SELECT DISTINCT teacher from student_academic_info where teacher like '" + incoming_name + "%';"
        print(query)
        cur.execute(query)
        row = cur.fetchall()
        teacher_name = row[0]['teacher']

        query = "SELECT username from users WHERE name='" + teacher_name + "';"
        print(query)
        cur.execute(query)
        row = cur.fetchall()
        teacher_id = row[0]['username']
        return 'teacher' + teacher_id + teacher_name

    elif matched_intent == 'contact_subject_teacher':
        print(response)
        incoming_name = response.query_result.parameters.fields['subject_name'].string_value
        print(response.query_result.parameters.fields)
        cur = db.connection.cursor()
        query = "SELECT DISTINCT teacher from student_academic_info where subject = '" + incoming_name + "';"
        print(query)
        cur.execute(query)
        row = cur.fetchall()
        teacher_name = row[0]['teacher']

        query = "SELECT username from users WHERE name='" + teacher_name + "';"
        print(query)
        cur.execute(query)
        row = cur.fetchall()
        teacher_id = row[0]['username']
        return 'teacher' + teacher_id + teacher_name

    elif matched_intent == 'subject_to_teacher':
        subject = response.query_result.parameters.fields['subject'].string_value
        print(subject)
        cur = db.connection.cursor()
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
        cur = db.connection.cursor()
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
        cur = db.connection.cursor()
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
        cur = db.connection.cursor()
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

        sql = 'SELECT * FROM users where username = "{}";'.format(username)
        cur = db.connection.cursor()
        cur.execute(sql)
        data = cur.fetchall()[0]
        print(data)
        if data['password'] == str(password):
            update_sql = 'update digital_signature set is_signed = 1 where username = "{}";'.format(username)
            print(update_sql)
            cur.execute(update_sql)
            db.connection.commit()
            resp = 'Successfully signed the report card!'
        else:
            resp = 'Invalid password'

    elif matched_intent == 'placement':
        params = response.query_result.parameters.fields['extremes'].string_value
        print(params)
        if params == '':
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM placement")
            row = cur.fetchall()
            companies = ''
            for tuples in row:
                companies += tuples['company_name'] + "  " + str(tuples['no_student_placed']) + "  " + str(tuples['package_offered']) + '\n'
            resp = companies
        elif params == 'highest':
            cur = db.connection.cursor()
            cur.execute("SELECT package_offered FROM placement")
            row = cur.fetchall()
            maxi = []
            for tuples in row:
                maxi.append(tuples['package_offered'])
            max_package = max(maxi)
            cur = db.connection.cursor()
            query = "SELECT company_name, no_student_placed FROM placement WHERE package_offered="+str(max_package)+";"
            cur.execute(query)
            row = cur.fetchall()
            resp = 'Highest package of ' + str(max_package) + ' was offered by ' + row[0]['company_name'] + ' to ' + str(row[0]['no_student_placed']) + '  students'
        elif params == 'lowest':
            cur = db.connection.cursor()
            cur.execute("SELECT package_offered  FROM placement")
            row = cur.fetchall()
            mini = []
            for tuples in row:
                mini.append(tuples['package_offered'])
            min_package = min(mini)
            cur = db.connection.cursor()
            query = "SELECT company_name, no_student_placed FROM placement WHERE package_offered=" + str(
                min_package) + ";"
            cur.execute(query)
            row = cur.fetchall()
            resp = 'Lowest package of ' + str(min_package) + ' was offered by ' + row[0]['company_name'] + ' to ' + str(row[0]['no_student_placed']) + '  students'

    elif matched_intent == 'fees':
        pass

    elif matched_intent == "progress":
        cur = db.connection.cursor()
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
