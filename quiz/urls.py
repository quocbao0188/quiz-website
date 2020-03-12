from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('quiz/<int:id>/', views.quiz, name='quiz'),
]
