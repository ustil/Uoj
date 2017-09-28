from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^search/', views.search, name='search'),
    #url(r'^/notice/$', views.noticeList, name='notice'),
]
