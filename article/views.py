from django.shortcuts import render
from django.shortcuts import HttpResponse
from datetime import datetime
# Create your views here.
def detail(request,article_id):
    return HttpResponse(article_id)

