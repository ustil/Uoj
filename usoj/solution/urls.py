from django.conf.urls import url
from . import views
from django.conf.urls.static import static
import usoj.settings

urlpatterns = [
    url(r'^$', views.solutionList, name='solution'),
    url(r'^my/', views.mySolution, name='mysolution'),
    url(r'^getcode/', views.getCode, name='getCode'),
    url(r'^getstatus/', views.getStatus, name='status'),
]


urlpatterns += static(usoj.settings.MEDIA_URL,
                      document_root=usoj.settings.MEDIA_ROOT)
