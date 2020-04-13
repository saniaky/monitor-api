import os

from sendgrid import SendGridAPIClient, Mail

sg = SendGridAPIClient()

base_url = os.environ.get('WEBSITE_URL')
from_email = os.environ.get('FROM_EMAIL')


def welcome_email(user):
    message = Mail(from_email=from_email, to_emails=user.email)
    message.template_id = 'd-a97bb89a6bfe44fda4deba762ef6a424'
    message.dynamic_template_data = {
        'name': user.first_name,
        'url': base_url + '/confirm-email?token=' + user.email_verification_token
    }
    sg.send(message)


def email_verified(user):
    message = Mail(from_email=from_email, to_emails=user.email)
    message.template_id = 'd-334a83d006384639ad4e27d138f4de18'
    message.dynamic_template_data = {
        'name': user.first_name,
        'url': base_url
    }
    sg.send(message)


def forgot_password(user):
    message = Mail(from_email=os.environ.get('FROM_EMAIL'), to_emails=user.email)
    message.template_id = 'd-f626293dd98649d6b6d53a5aa3a355d4'
    message.dynamic_template_data = {
        'name': user.first_name,
        'url': base_url + '/reset-password?token=' + user.password_reset_token
    }
    sg.send(message)


def password_changed(user):
    message = Mail(from_email=os.environ.get('FROM_EMAIL'), to_emails=user.email)
    message.template_id = 'd-a2772ca6568e4d3ba14efede9d83c422'
    message.dynamic_template_data = {
        'name': user.first_name
    }
    sg.send(message)
