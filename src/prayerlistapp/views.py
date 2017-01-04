from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse
import datetime

from . import models

def index(request):
	prs = models.PrayerRequest.objects.all()
	return render(
		request, 
		'index.html',
		{
			'prayer_requests': prs,
		}
	)

def current_datetime(request):
	now = datetime.datetime.now()
	t = Template('<html><body>It is now {{ current_date }}. </body></html>')
	html = t.render(Context({'current_date' : now}))
	return HttpResponse(html)
