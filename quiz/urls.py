from django.urls import path
# from .views import QuizLikeRedirectView, QuizLikeAPIToggle, QuizListView
from . import views
from django.conf.urls import url

urlpatterns = [
    path('luyen-thi/', views.quiz_list, name='quiz'),
    # path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    # path('quiz/<int:pk>/like/', QuizLikeRedirectView.as_view(), name='quiz-like'),
    url(r'^thong-tin-bai-thi/(?P<slug>[\w-]+)/$', views.pre_quiz, name='pre-quiz'),
    url(r'^luyen-thi/(?P<slug>[\w-]+)/$', views.quiz_detail, name='quiz-detail'),
    url(r'^luyen-thi/xem-dap-an/(?P<slug>[\w-]+)/$', views.see_answer, name='see-answer'),
    url(r'^chuyen-muc-bai-thi/(?P<slug>[\w-]+)/$', views.catago_quiz, name='catago-quiz'),
    path('bang-diem/', views.transcript_show, name='transcript'),
    url(r'^delete/(?P<id>\d+)/$', views.del_transcript, name='del-transcript'),
    url(r'^bang-diem/chi-tiet-bang-diem/(?P<slug>[\w-]+)/$', views.transcript_detail, name='transcript-detail'),
    # url(r'^quiz/(?P<slug>[\w-]+)/like/$', QuizLikeRedirectView.as_view(), name='quiz-like'),
    # url(r'^api/quiz/(?P<slug>[\w-]+)/like/$', QuizLikeAPIToggle.as_view(), name='quiz-api-like'),
]
