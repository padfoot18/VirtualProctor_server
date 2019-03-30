from flask import Flask, request, jsonify
import config
import requests
from flask_mysqldb import MySQL
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


@app.route('/chat', methods=['POST'])
def chat():
    query = request.form['query']
    print(query)
    return ""
    # req = request.get_json(silent=True, force=True)
    # matched_intent = req['queryResult']['intent']['displayName']
    # if matched_intent == 'event_query':
    #     print(matched_intent)
    #     return jsonify({"fulfillmentText": "no events"})


if __name__ == '__main__':
    app.run(debug=True)
