from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),	
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),
    url(r'^now/$', views.current_datetime),
]