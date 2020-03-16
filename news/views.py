from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import News


def Homepage(request):
    return render(request, 'myblog.html')

def news_list(request):
    news = News.objects.all()
    context = {'news': news, }
    return render(request, 'news/list.html', context)

def news_detail(request, id):
    news = News.objects.get(id)
    context = {'news': news, }
    return render(request, 'news/detail.html', context)