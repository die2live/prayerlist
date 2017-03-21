from celery.decorators import task, periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.db.models import Q
from datetime import datetime
from itertools import groupby

from .models import PrayerRequest
from .emails import send_daily_email, send_periodic_email

logger = get_task_logger(__name__)

#@task(name='send_daily_email_task')
@periodic_task(run_every=(crontab(minute=28, hour=10)), name='periodic task', ignore_result=True)
def send_daily_email_task():
    '''
    Send an email with prayer needs specified for current date
    '''
    logger.info('get daily email data')
    pr_for_today = PrayerRequest.objects.filter(
                    Q(deleted_date=None),
                    Q(show_date=datetime.today())
                    )
    logger.info('send daily email')
    for key, values in groupby(pr_for_today, key=lambda row: row.created_by.user.email):
        logger.info('send daily email for %s' % key)
        send_daily_email(key, values)






#@periodic_task(run_every=(crontab(minute=45, hour=8)), name='periodic task', ignore_result=True)
#def periodic_task():
#    logger.info('run periodic task')
#    return send_periodic_email('alexandr.dermenji@gmail.com', "my message")