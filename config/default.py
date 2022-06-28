import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')

CORS_HEADERS = 'Content-Type'

PROPAGATE_EXCEPTIONS = True

URL_INITIAL = os.getenv('WEBSITE')

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False
ERROR_404_HELP = False
SQLALCHEMY_POOL_RECYCLE = 299

# Configuración del email
MAIL_SERVER = ''
MAIL_PORT = 0
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_USE_SSL = True
MAIL_DEBUG = False
DONT_REPLY_FROM_EMAIL = ''
ADMINS = ''
