from flask_mail import Message, Mail

mail = Mail()


def init_mail(app):
    mail.init_app(app)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
