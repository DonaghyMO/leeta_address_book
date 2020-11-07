from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
def detail(request,article_id):
    return HttpResponse(article_id)