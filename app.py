from flask import Flask, request, jsonify
import config
from flask_mysqldb import MySQL
import dialogflow_v2 as dialogflow
import os


app = Flask(__name__)


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

    elif matched_intent == 'Default Welcome Intent':
        resp = response.query_result.fulfillment_text
    elif matched_intent == 'Default Fallback Intent':
        resp = response.query_result.fulfillment_text

    return resp


if __name__ == '__main__':
    app.run(debug=True)
