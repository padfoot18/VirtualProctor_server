from flask import request, jsonify
from app import db
from app.chat import chat_bp
from app.push_notification.notifications import send_notification


@chat_bp.route('/chat_list')
def get_open_chats():
    username = request.args.get('username')
    sql1 = 'SELECT distinct from_user from chats where to_user = "{}";'.format(username)
    sql2 = 'SELECT distinct to_user from chats where from_user = "{}";'.format(username)
    cur = db.connection.cursor()
    now_of_rows1 = cur.execute(sql1)
    print(sql1)
    print(sql2)
    open_chats = set()
    if now_of_rows1 > 0:
        data1 = cur.fetchall()
        print('data1', data1)
        for row in data1:
            if row['from_user'] != username:
                open_chats.add(row['from_user'])

    no_of_rows2 = cur.execute(sql2)
    if no_of_rows2 > 0:
        data2 = cur.fetchall()
        print('data2', data2)
        for row in data2:
            if row['to_user'] != username:
                open_chats.add(row['to_user'])

    open_chats = list(open_chats)
    print(open_chats)
    sql = 'SELECT username, name from users where username in ("{}");'.format('", "'.join(open_chats))
    print(sql)
    now_of_rows = cur.execute(sql)

    if now_of_rows > 0:
        data = cur.fetchall()
        print(data)

        return jsonify(data)
    else:
        return jsonify({})


@chat_bp.route('/get_all_chats')
def get_all_chats():
    user1 = request.args.get('user1')
    user2 = request.args.get('user2')
    sql = '''SELECT * FROM chats where (from_user = "{}" and to_user = "{}") or (from_user = "{}" and to_user = "{}");'''.format(user1, user2, user2, user1)
    # TODO: handle reverse messages in android
    cur = db.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return jsonify(data)


@chat_bp.route('/insert_chat', methods=['POST'])
def add_chat():
    temp_result = request.get_json()
    from_user = temp_result['from_user']
    print(from_user)
    to_user = temp_result['to_user']
    msg_body = temp_result['msg_body']
    password = temp_result['password']

    sql = 'SELECT * FROM users where username = "{}";'.format(from_user)
    cur = db.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()[0]
    print(data)
    if data['password'] == password:
        insert_sql = 'INSERT into chats (from_user, to_user, msg_body) values ("{}", "{}", "{}");'.format(from_user,
                                                                                                          to_user,
                                                                                                          msg_body)
        print(insert_sql)
        cur.execute(insert_sql)
        db.connection.commit()
        send_notification(to_user, 'New message', msg_body, 'user')
        cur.close()
        return jsonify({'success': True})


@chat_bp.route('/broadcast_to_group', methods=['POST'])
def broadcast_msg():
    form_data = request.get_json()
    from_user = form_data['from_user']
    password = form_data['password']
    group_id = form_data['group_id']
    message = form_data['msg_body']

    sql = 'SELECT * FROM users where username = "{}";'.format(from_user)
    cur = db.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()[0]
    print(data)
    if data['password'] == password:
        insert_sql = 'INSERT INTO broadcast_msg (from_id, group_id, msg_body) values ("{}", "{}", "{}");'.format(
            from_user, group_id, message)
        print(insert_sql)
        cur = db.connection.cursor()
        cur.execute(insert_sql)
        db.connection.commit()
        send_notification(group_id, 'New broadcast message', message, 'group')
        return jsonify({'success': 1})


@chat_bp.route('/get_broadcast_msg', methods=['GET'])
def get_broadcast_msg():
    username = request.args.get('username')
    sql = '''SELECT group_id, msg_body, msg_time, name FROM broadcast_msg natural join groups join users on from_id = username where group_id in (
    SELECT group_id from user_to_group where username = "{}") order by msg_time desc limit 10;'''.format(username)
    print(sql)

    cur = db.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    return jsonify(data)


@chat_bp.route('/get_groups', methods=['GET'])
def get_groups():
    sql = 'SELECT * from groups;'
    cur = db.connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    return jsonify(data)
