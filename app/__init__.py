from flask import Flask
from config import Config
from flask_mysqldb import MySQL
from pyfcm import FCMNotification
from personal_config import api_keys

db = None
push_service = None

# TODO IMPORTANT: USE url_for(function_name) for dynamic urls!!!
# TODO: Encrypt passwords lol


def create_app(config_class=Config):
    global db
    global push_service

    app = Flask(__name__)
    app.config.from_object(config_class)
    db = MySQL(app)
    push_service = FCMNotification(api_keys['fcm'])

    from app.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    from app.push_notification import notif_bp
    app.register_blueprint(notif_bp, url_prefix='/notification')

    from app.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.chatbot import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

    return app
