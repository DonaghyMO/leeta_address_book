from django.shortcuts import HttpResponse
from django.http import Http404
from django.shortcuts import render
from .models import Article
def detail(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except Article.DoesNotExist:
        raise Http404("article doesn't exists")
    print(article)
    return HttpResponse(article.content)

def get_articles(request):
    articles = Article.objects.all()
    context = {
        "article_list":articles,
        "title":"我的天哪！",
    }
    return render(request,'article/index.html',context)