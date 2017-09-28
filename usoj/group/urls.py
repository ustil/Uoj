from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^create/', views.createGroup, name='creatGroup'),
    url(r'^$', views.groupList, name='groupList'),
    url(r'^join/', views.joinGroup, name='joinGroup'),
    url(r'^mygroup/', views.myGroup, name='mygroup'),
    url(r'^del_(?P<id>\d+)/', views.delGroup, name='delGroup'),
    url(r'^kick_(?P<id>\d+)/', views.kickGroup, name='delGroup'),

    url(r'^audit/allow_(?P<id>\d+)/', views.auditAllow, name='auditAllow'),
    url(r'^audit/reject_(?P<id>\d+)/', views.auditReject, name='auditReject'),
]
