from django.urls import path
from .views import QuizListView, QuizDetailView
from . import views

urlpatterns = [
    #path('', views.index, name='home'),
    path('quiz/', QuizListView.as_view(), name='quiz'),
    #path('quiz/<int:id>/', views.quiz, name='quiz'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
]
