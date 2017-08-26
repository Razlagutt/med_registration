from django.conf.urls import url
from . import views


app_name = 'registration_app'

urlpatterns = [
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^registration/$', views.user_register, name='user_register'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^doctors/$', views.doctors_list, name='doctors'),
    url(r'^doctors/(?P<id>\d+)/$', views.schedule, name='schedule'),
]