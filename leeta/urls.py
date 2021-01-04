from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$',index),
    url(r'show_enterprises/',enterprises_show),
    url(r'^search/$', enterprises_search),
    url(r'^update/',enterprise_update,),
    url(r'^login/',login),
]