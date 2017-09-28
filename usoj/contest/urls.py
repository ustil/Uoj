from django.conf.urls import patterns, url
from . import views
from index.views import addNotice

urlpatterns = [
    url(r'^$', views.contestList, name='contestList'),
    url(r'^password/(?P<id>\d+)/', views.contestPassword, name='contestPassword'),
    url(r'^detail/(?P<id>\d+)/', views.contestDetail, name='contestDetail'),
    url(r'^group/(?P<id>\d+)/', views.contestGroup, name='contestGroup'),
    url(r'^submit/(?P<id>\d+)/', views.contestSubmit, name='contestSubmit'),
    url(r'^solution/(?P<id>\d+)/', views.contestSolution, name='contestSolution'),
    url(r'^rank/(?P<id>\d+)/', views.contestRank, name='contestRank'),
    url(r'^problem/(?P<id>\d+)/', views.contestProblem, name='contestRroblem'),
    url(r'^notice/', views.notice, name='contestnotice'),
    url(r'^choose/', views.chooseGroup, name='chooseGroup'),

    url(r'^enrollGroup/(?P<id>\d+)/', views.enrollGroup, name='enrollGroup'),
    url(r'^enrollPerson/(?P<id>\d+)/', views.enrollUser, name='enrollUser'),

    #url(r'^addnotice/', addNotice, name='addnotice'),
]
