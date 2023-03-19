from django.core.mail import mail_admins

from website.celery import app


@app.task
def task_email_to_admin(title, msg):
    """ Отправляет email администратору сайта. """
    mail_admins(title, msg,
                fail_silently=False,
                connection=None,
                html_message=None
                )
