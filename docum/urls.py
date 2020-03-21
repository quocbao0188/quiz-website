from django.urls import path
from . import views
from .views import DocListView

urlpatterns = [
    path('documents/', DocListView.as_view(), name='documents'),
]

    