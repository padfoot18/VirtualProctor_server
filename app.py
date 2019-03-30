from flask import Flask, request, jsonify
import requests
from flask_mysqldb import MySQL
app = Flask(__name__)

# config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'VirtualProctor'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# initialize MYSQL
mysql = MySQL(app)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/android_login', methods=['POST'])
def android_login():
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)

    cur = mysql.connection.cursor()
    query_result = cur.execute("SELECT * FROM users WHERE username=%s", [username])
    if query_result == 1:
        row = cur.fetchall()
        passwd = row['password']
        role = row['role']
        if password == passwd:
            return "{\"flag\":\"true\", \"role\":"+role+"}";
        else:
            return "{\"flag\":\"password_false\", \"role\":\"None\"}";
        mysql.connection.commit()
        cur.close()
    else:
        return "{\"flag\":\"username_false\", \"role\":\"None\"}";


@app.route('/chat', methods=['POST'])
def chat():
    req = request.get_json(silent=True, force=True)
    matched_intent = req['queryResult']['intent']['displayName']
    print(matched_intent)
    if matched_intent == 'events':
        '''
            Code to fetch events from database
        '''
        event_data = "Prakalpa\nAbhiyantriki\nSymphony\n\nTell me the event name to know more"
        return jsonify({"fulfillmentText": event_data})
    return

if __name__ == '__main__':
    app.run(debug=True)
