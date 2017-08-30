from django.conf.urls import url
from . import views


app_name = 'registration'

urlpatterns = [
    url(r'^$', views.user_login, name='user_login'),
    url(r'^registration/$', views.user_register, name='user_register'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^doctors/$', views.doctors, name='doctors'),
    url(r'^(?P<id>\d+)/$', views.schedule, name='schedule'),
    url(r'^(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$', views.record, name='record_list'),
]