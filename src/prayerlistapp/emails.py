from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string


def send_daily_email(email, prayer_requests):
    context = Context({ 'prayer_requests': prayer_requests })
    email_subject = render_to_string('email/daily_email_subject.html', context)
    email_body = render_to_string('email/daily_email_body.html', context)

    return send_mail(
        email_subject,              # subject
        email_body,                 # message
        settings.EMAIL_HOST_USER,   # from_email
        [email],                    # recipient_list
        fail_silently=False,
        html_message=email_body
    )

def send_test_email():
    return send_mail(
        'Test celery',                  # subject
        'Test celery body',             # message
        settings.EMAIL_HOST_USER,       # from_email
        [settings.EMAIL_HOST_USER],     # recipient_list
        fail_silently=False
    )