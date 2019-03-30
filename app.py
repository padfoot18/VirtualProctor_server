from flask import Flask, request

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
        return "{\"flag\":\"true\", \"role\":\"user\"}";
    if username != "abcd" and password != "1234":
        return "{\"flag\":\"both_false\", \"role\":\"None\"}";
    elif username != "abcd":
        return "{\"flag\":\"username_false\", \"role\":\"None\"}";
    elif password != "1234":
        return "{\"flag\":\"password_false\", \"role\":\"None\"}";


if __name__ == '__main__':
    app.run(debug=True)
