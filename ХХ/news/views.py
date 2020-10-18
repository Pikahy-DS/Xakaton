from django.shortcuts import render
from .models import Artiles1


def news_home(request):
    news = Artiles1.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})
