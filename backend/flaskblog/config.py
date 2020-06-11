import os
import json

with open('/etc/config.json') as config_file:
    conf = json.load(config_file)

class Config:
    SECRET_KEY = conf.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = conf.get('SECURITY_PASSWORD_SALT')
    SQLALCHEMY_DATABASE_URI = conf.get('SQLALCHEMY_DATABASE_URI')
    API_URL = conf.get('API_URL')
    X_MYSQL_PASS = conf.get('X_MYSQL_PASS')
    X_MYSQL_USER = conf.get('X_MYSQL_USER')
    X_MYSQL_HOST = conf.get('X_MYSQL_HOST')

    MAIL_SERVER = 'smtp.googlemail.com'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = conf.get('EMAIL_USER')
    MAIL_PASSWORD = conf.get('EMAIL_PASS')
