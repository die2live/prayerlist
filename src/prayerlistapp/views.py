from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse
import datetime

def index(request):
	return HttpResponse("Hello world!")

def current_datetime(request):
	now = datetime.datetime.now()
	t = Template('<html><body>It is now {{ current_date }}. </body></html>')
	html = t.render(Context({'current_date' : now}))
	return HttpResponse(html)
