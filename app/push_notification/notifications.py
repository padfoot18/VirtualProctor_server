from app import db
from flask import request
from app.push_notification import notif_bp
from app import push_service


def send_notification(to, message_title, message_body, receiver_type='user'):
    cur = db.connection.cursor()
    if to == 'all':
        query = 'SELECT * from username_to_fcmId;'
    elif receiver_type == 'user':
        query = 'SELECT * from username_to_fcmId where username="{}";'.format(to)
    elif receiver_type == 'group':
        query = 'SELECT * FROM username_to_fcmId natural join user_to_group where group_id = "{}";'.format(to)

    no_of_rows = cur.execute(query)
    if no_of_rows > 0:
        data = cur.fetchall()
        print(data)
        registration_ids = []
        for row in data:
            registration_ids.append(row['fcm_id'])

        print(registration_ids)

        result = push_service.notify_multiple_devices(
            registration_ids=registration_ids,
            message_title=message_title,
            message_body=message_body
        )
        print(result)
        return result
    else:
        return {'success': 0}


# TODO: change get request to post request
@notif_bp.route('/register', methods=['GET'])
def register():
    username = request.args.get('username')
    fcm_id = request.args.get('fcm_id')

    # update in the database
    # create cursor
    cur = db.connection.cursor()
    cur.execute('DELETE FROM username_to_fcmId WHERE username="{}";'.format(username))
    cur.execute('INSERT IGNORE INTO username_to_fcmId(username, fcm_id) VALUES("{}", "{}");'.format(username, fcm_id))
    db.connection.commit()
    cur.close()
    return "Update Success"
