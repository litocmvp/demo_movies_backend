from .default import *
import os
from dotenv import load_dotenv

load_dotenv()

# APP_ENV = APP_ENV_DEVELOPMENT
SECRET_KEY = os.getenv('KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')

URL_INITIAL = os.getenv('WEBSITE')

# Configuración del email
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USERNAME = os.getenv('MAIL_USER')
MAIL_PASSWORD = os.getenv('MAIL_PASS')
DONT_REPLY_FROM_EMAIL = os.getenv('MAIL_DONT_REPLY')
ADMINS = os.getenv('MAIL_ADMIN')