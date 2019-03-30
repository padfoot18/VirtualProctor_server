from config import fcm_config
from pyfcm import FCMNotification


def send_notification_all(message_title, message_body):
    push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,
                                         message_body=message_body)
