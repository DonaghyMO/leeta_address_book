"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from article import views as article_views
from test_love import views as test_love_views
from index import views as index_views
urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^(?P<article_id>\d+)/$', article_views.detail),
    url(r'show_love/',test_love_views.test),
    url(r'^$',index_views.index),
]
