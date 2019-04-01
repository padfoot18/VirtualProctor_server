from flask import Flask
from config import Config
from flask_mysqldb import MySQL
from pyfcm import FCMNotification

db = None
push_service = None


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db = MySQL(app)
    push_service = FCMNotification(app)

    from app.chat import chat_bp
    app.register_blueprint(chat_bp)

    from app.push_notification import notif_bp
    app.register_blueprint(notif_bp)

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.chatbot import chatbot_bp
    app.register_blueprint(chatbot_bp)

    return app
