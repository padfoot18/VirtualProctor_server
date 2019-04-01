from flask import Blueprint


notif_bp = Blueprint('notification', __name__)


from app.push_notification import notifications
