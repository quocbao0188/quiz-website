from django.urls import path
from django.conf.urls import url
# from .views import HomeListView
from . import views

urlpatterns = [
    path('', views.index, name='home'),
]
