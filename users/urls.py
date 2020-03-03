from django.urls import path
from . import views as users_view

urlpatterns = [
    path('', users_view.register, name='register'),
]