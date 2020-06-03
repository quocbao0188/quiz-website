from django.conf.urls import url
from django.contrib  import admin
from django.urls import path
from search import views

urlpatterns = [
    path('input-search/', views.search, name='input-search'),
    url(r'^$', views.search_docs, name='search-docs'),
]