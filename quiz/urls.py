from django.urls import path
# from .views import QuizLikeRedirectView, QuizLikeAPIToggle, QuizListView
from . import views
from django.conf.urls import url

urlpatterns = [
    # path('', views.index, name='home'),
    path('quiz/', views.quiz_list, name='quiz'),
    # path('quiz/', views.quiz, name='quiz'),
    # path('quiz/<int:id>/', views.quiz_detail, name='quiz-detail'),
    # path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    #path('quiz/<int:pk>/like/', QuizLikeRedirectView.as_view(), name='quiz-like'),
    url(r'^pre-quiz/(?P<slug>[\w-]+)/$', views.pre_quiz, name='pre-quiz'),
    url(r'^quiz/(?P<slug>[\w-]+)/$', views.quiz_detail, name='quiz-detail'),
    url(r'^quiz/see-answer/(?P<slug>[\w-]+)/$', views.see_answer, name='see-answer'),
    url(r'^catagories-quiz/(?P<slug>[\w-]+)/$', views.catago_quiz, name='catago-quiz'),
    path('transcript/', views.transcript_show, name='transcript'),
    # url(r'^quiz/(?P<slug>[\w-]+)/like/$', QuizLikeRedirectView.as_view(), name='quiz-like'),
    # url(r'^api/quiz/(?P<slug>[\w-]+)/like/$', QuizLikeAPIToggle.as_view(), name='quiz-api-like'),
]
