from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^add/', views.addProblem, name='addproblem'),
    # url(r'^xml/', views.updateXMl, name='updatexmls'),
    url(r'^$', views.problemList, name='problemList'),
    # url(r'^edit/(?P<id>\d+)/', views.editProblem, name='editProblem'),
    url(r'^detail/', views.problemDetail, name='problemDetail'),
    url(r'^solution/', views.problemSolution, name='problemSolution'),
    url(r'^submit/', views.problemSubmit, name='problemSubmit'),
]
