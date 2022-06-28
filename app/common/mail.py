import logging
from smtplib import SMTPException
from threading import Thread
from flask import current_app
from flask_mail import Mail, Message
from queue import Queue

mail = Mail()

logger = logging.getLogger(__name__)

def _send_async_email(app, msg, queue):
    with app.app_context():
        try:
            mail.send(msg)
            salida = True
        except SMTPException:
            logger.exception("Ocurrió un error al enviar el email")
            salida = False
        queue.put(salida)

def send_email(subject, sender, recipients, text_body, cc=None, bcc=None, html_body=None, \
    file=None, filename=None, typefile=None):
    msg = Message(subject, sender=sender, recipients=recipients, cc=cc, bcc=bcc)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    if file:
        with current_app.open_resource(file) as fp:
            msg.attach(filename, typefile, fp.read())
    queue = Queue()
    hilo= Thread(target=_send_async_email, args=(current_app._get_current_object(), msg, queue))
    hilo.start()
    hilo.join()
    retorno = queue.get()
    return retorno