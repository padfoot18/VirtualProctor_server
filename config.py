from personal_config import flask_config, mysql_config


class Config(object):
    """
    Flask config class
    """
    SECRET_KEY = flask_config['secret_key']
    MYSQL_HOST = mysql_config['host']
    MYSQL_USER = mysql_config['user']
    MYSQL_PASSWORD = mysql_config['password']
    MYSQL_DB = mysql_config['database']
    MYSQL_CURSORCLASS = mysql_config['cursor_class']
