from .feeds import LatestPostsFeed
from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path("reader/", views.read_rss, name="reader")
]