"""__init__.py initializes script of the app package
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import views, models

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler

    # file handler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

    # mail handler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-reply@' + MAIL_SERVER,
                               ADMINS,
                               'microblog failure',
                               credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
