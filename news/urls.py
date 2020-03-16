from django.urls import path
from . import views


app_name = 'news'

urlpatterns = [
    path('', views.Homepage, name='homepage'),
    path('news_list/', views.news_list, name='news_list'),
    path('news_detail/<int:id>/', views.news_detail, name='news_detail'),
]