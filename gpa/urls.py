from django.urls import path
from . import views

urlpatterns = [
    path('gpa/', views.calculator, name='gpa')
]