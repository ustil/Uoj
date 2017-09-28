from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.solutionList, name='solution'),
    url(r'^my/', views.mySolution, name='mysolution'),
    url(r'^getcode/', views.getCode, name='getCode'),
    url(r'^getstatus/', views.getStatus, name='status'),
]

from django.conf.urls.static import static
import usoj.settings

urlpatterns += static(usoj.settings.MEDIA_URL, document_root=usoj.settings.MEDIA_ROOT)
