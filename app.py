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
        return "true"
    if username != "abcd" and password != "1234":
        return "both_false"
    elif username != "abcd":
        return "username_false"
    elif password != "1234":
        return "password_false"


if __name__ == '__main__':
    app.run()
