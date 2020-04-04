# from django.urls import path
# from .views import QuizLikeRedirectView, QuizLikeAPIToggle, QuizListView
# from . import views
# from django.conf.urls import url

# urlpatterns = [
#     # path('', views.index, name='home'),
#     path('quiz/', QuizListView.as_view(), name='quiz'),
#     # path('quiz/', views.quiz, name='quiz'),
#     # path('quiz/<int:id>/', views.quiz_detail, name='quiz-detail'),
#     # path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
#     #path('quiz/<int:pk>/like/', QuizLikeRedirectView.as_view(), name='quiz-like'),
#     url(r'^quiz/(?P<slug>[\w-]+)/$', views.quiz_detail, name='quiz-detail'),
#     url(r'^quiz/(?P<slug>[\w-]+)/like/$', QuizLikeRedirectView.as_view(), name='quiz-like'),
#     url(r'^api/quiz/(?P<slug>[\w-]+)/like/$', QuizLikeAPIToggle.as_view(), name='quiz-api-like'),
# ]
