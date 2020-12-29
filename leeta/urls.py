from django.conf.urls import url
from .views import index,enterprises_show
urlpatterns = [
    url(r'^$',index),
    url(r'show_enterprises/',enterprises_show)
]