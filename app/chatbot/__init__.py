from flask import Blueprint


chatbot_bp = Blueprint('chatbot', __name__)


from app.chatbot import routes
