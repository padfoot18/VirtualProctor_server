from flask import Flask, request, jsonify
import requests
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)

    if username == "abcd" and password == "1234":
        return "true"
    if username != "abcd" and password != "1234":
        return "both_false"
    elif username != "abcd":
        return "username_false"
    elif password != "1234":
        return "password_false"


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
    app.run(debug='True')
