from django.conf import settings
from django.core.mail import send_mail
#from django.template import Context
#from django.template.loader import render_to_string


def send_daily_email(email, prayer_requests):
    email_subject = 'Daily Prayer List'

    m = ''
    for p in prayer_requests:
        m += "%s || " % p


    email_body = 'These are your prayer needs for today! %s' % m

    return send_mail(
        email_subject,              # subject
        email_body,                 # message
        settings.EMAIL_HOST_USER,   # from_email
        [email],                    # recipient_list
        fail_silently=False
        #html_message=''
    )

def send_periodic_email(email, message):
    email_subject = 'Periodic email'
    email_body = message

    return send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)

