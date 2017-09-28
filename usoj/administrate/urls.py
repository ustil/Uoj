from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^problem/', views.showProblem, name='manageshowproblem'),
    url(r'^contest/', views.showContest, name='manageshowcontest'),
    url(r'^notice/', views.showNotice, name='manageshownotice'),
    url(r'^group/', views.showGroup, name='manageshowgroup'),
    url(r'^judger/', views.showJudger, name='manageshowjudger'),
    url(r'^account/', views.showAccount, name='manageshowaccount'),

    url(r'^add/problem/', views.addProblem, name='manageaddproblem'),
    url(r'^add/xmlproblem/', views.addxmlProblem, name='manageaddproblem'),
    url(r'^add/contest/', views.addContest, name='manageaddcontest'),
    url(r'^add/notice/', views.addNotice, name='manageaddnotice'),
    url(r'^add/judger/', views.addJudger, name='manageaddjudger'),
    url(r'^add/account/', views.addAccount, name='manageaddaccount'),

    url(r'^edit/problem/', views.editProblem, name='manageeditproblem'),
    url(r'^edit/contest/', views.editContest, name='manageeditcontest'),
    url(r'^edit/notice/', views.editNotice, name='manageeditnotice'),
    url(r'^edit/group/', views.editGroup, name='manageeditgroup'),
    url(r'^edit/judger/', views.editJudger, name='manageeditjudger'),
    url(r'^edit/account/', views.editAccount, name='manageeditaccount'),

    url(r'^rm/problem/', views.rmProblem, name='managermproblem'),
    url(r'^rm/contest/', views.rmContest, name='managermcontest'),
    url(r'^rm/notice/', views.rmNotice, name='managermnotice'),
    url(r'^rm/group/', views.rmGroup, name='managermgroup'),
    url(r'^rm/judger/', views.rmJudger, name='managermjudger'),

    url(r'^rejudge/', views.rejudge, name='managerejudge'),

    url(r'^downloadtest/', views.downloadtest, name='downloadtest'),
    url(r'^changeshow/', views.changeshow, name='changeshow'),
    url(r'^$', views.index, name='manageindex'),
]
