from django.conf.urls import url
from django.contrib  import admin
from .views import search_docs

urlpatterns = [
    url(r'^$', search_docs, name='search-docs'),
]