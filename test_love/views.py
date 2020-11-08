from django.shortcuts import render
from datetime import datetime

# Create your views here.

def test(request):
    return render(request,'show_love.html',{'current_time': datetime.now()})
