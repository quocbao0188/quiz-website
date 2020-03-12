from django.urls import path
from . import views

urlpatterns = [
    path('sharing/', views.sharing, name='sharing'),
]