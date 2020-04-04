from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('documents/', views.document_list, name='documents'),
    url(r'^document/(?P<slug>[\w-]+)/$', views.document_detail, name='doc-detail'),
]

    