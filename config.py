"""config.py contains the configuration of the app
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/microblog'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_ENABLED = True
SECRET_KEY = 'iouy4949SLDaDJAKSDLvka38LAK8g4ds8'
SECURITY_REGISTERABLE = True
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = b'asdkwe'
SECURITY_USER_IDENTITY_ATTRIBUTES = ['email', 'username']
SECURITY_SEND_REGISTER_EMAIL = False

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = 'yuraist'
MAIL_PASSWORD = 'qwerty123'

# administrator list
ADMINS = ['yura.ist@icloud.com']

UPLOAD_FOLDER = os.path.join(basedir, 'app/media')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

LANGUAGES = {
    'en': 'English',
    'ru': 'Russian'
}
