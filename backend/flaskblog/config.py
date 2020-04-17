import os
import json

with open('/etc/config.json') as config_file:
    conf = json.load(config_file)

class Config:
    SECRET_KEY = conf.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = conf.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = conf.get('EMAIL_USER')
    MAIL_PASSWORD = conf.get('EMAIL_PASS')
