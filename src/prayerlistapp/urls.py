from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),	
    url(r'^edit/(?P<id>\d)*(\/)*$', views.edit, name='edit'),	
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),    
]