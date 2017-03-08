from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),	
    url(r'^today/$', views.today, name='today'),	
    url(r'^all/$', views.all, name='all'),	
    url(r'^edit/(?P<pk>\d*)(\/*)$', views.edit, name='edit'),	
    url(r'^delete/(?P<id>\d*)(\/*)$', views.delete, name='delete'),
    url(r'^markread/(?P<id>\d*)(\/*)$', views.mark_as_read, name='mark_as_read'),
    url(r'^about/$', views.about, name='about'),	
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),    
]