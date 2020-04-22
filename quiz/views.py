from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import RedirectView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Quiz, Question, Answer, QuizProfile, AttemptedQuestion, CategoryQuiz
# from .forms import QuestionForm
# Create your views here.

def quiz_list(request):
    template_name = 'quiz/quiz.html'
    quiz = Quiz.objects.all().annotate(question_count=Count('questions'))
    context = {
        'quiz': quiz,
        'cata': CategoryQuiz.objects.all().annotate(docs_count=Count('quizs'))[:5],
        'most': Quiz.objects.order_by('-created').all()[:5],
    }
    return render(request, template_name, context)

def quiz_detail(request, slug=None):
    questions = []  #Tạo list chứa các câu hỏi để gởi xuống html
    template_name = 'quiz/quiz-detail.html'
    quiz = get_object_or_404(Quiz, slug=slug)   # Lấy cuộc thi được chọn
    que = Question.objects.filter(quiz_id=quiz.id)  # Chọn những câu hỏi trong kì thi
    for q in que:
        ans = Answer.objects.filter(question_id=q.id)   # Chọn bộ những câu trả lời thuộc câu hỏi
        question = {
            'label': q.label,
            'aidi': q.id,
            'answer': ans
        }
        questions.append(question)

    # quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        for z in que:
            answer_data = Answer.objects.filter(question_id=z.id)
            question_id = request.GET.get('question-' + str(z.id))
            choise_id = request.GET.get('choise-' + str(z.id))
            print(choise_id)

        

    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, template_name, context)

# def quiz_detail(request, slug=None):
#     questions = []          #Tạo list chứa các câu hỏi để gởi xuống html
#     template_name = 'quiz/quiz-detail.html'
#     quiz = get_object_or_404(Quiz, slug=slug)  # Lấy cuộc thi được chọn
#     que = Question.objects.filter(quiz_id=quiz.id)         # Chọn những câu hỏi trong kì thi
#     for q in que:               
#         ans = Answer.objects.filter(question_id=q.id)  # Chọn bộ những câu trả lời thuộc câu hỏi
#         question = {
#             'label': q.label,
#             'aidi': q.id,
#             'answer': ans
#         }
#         questions.append(question)
#     context = {
#         'quiz': quiz,
#         'questions': questions
#     }
#     return render(request, template_name, context)

# def quiz_detail(request, slug=None):
#     template_name = 'quiz/quiz-detail.html'
#     quiz = get_object_or_404(Quiz, slug=slug)
#     q = quiz.questions.all()
#     form_list = QuestionForm(instance=q)
#     context = {
#         'quiz': quiz,
#         'form_list': form_list,
#     }
#     return render(request, template_name, context)


# # List View Index
# class QuizListView(ListView):
#     model = Post
#     # <app>/<model>_<viewtype>.html
#     template_name = 'pages/quiz.html'
#     context_object_name = 'doc'
#     paginate_by = 2

# # class QuizDetailView(DetailView):
# #     model = Post
# #     template_name = 'pages/quiz-detail.html'

# class QuizLikeRedirectView(RedirectView):
#     def get_redirect_url(self, *args, **kwargs):
#         slug = self.kwargs.get("slug")
#         obj = get_object_or_404(Post, slug=slug)
#         urls_ = obj.get_absolute_url()
#         user = self.request.user
#         if user.is_authenticated:
#             if user in obj.likes.all():
#                 obj.likes.remove(user)
#             else:
#                 obj.likes.add(user)
#         return urls_

# class QuizLikeAPIToggle(APIView):
#     authentication_classes = [authentication.SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, slug=None, format=None):
#         # slug = self.kwargs.get("slug")
#         obj = get_object_or_404(Post, slug=slug)
#         urls_ = obj.get_absolute_url()
#         user = self.request.user
#         updated = False
#         liked = False
#         if user.is_authenticated:
#             if user in obj.likes.all():
#                 liked = False
#                 obj.likes.remove(user)
#             else:
#                 liked = True
#                 obj.likes.add(user)
#             updated = True

#         data = {
#             "updated": updated,
#             "liked": liked
#         }

#         return Response(data)


# # def quiz(request):
# #     template_name = 'pages/quiz.html'
# #     content = {
# #         'doc':  Post.objects.all()#.order_by('-date_posted')
# #     }
# #     return render(request, template_name, content)

# # class CataList(ListView):
# #     model = Catagories
# #     template_name = 'pages/widget.html'
# #     context_object_name = 'catalo'
    


# def quiz_detail(request, slug=None):
#     template_name = 'pages/quiz-detail.html'
#     post = {
#         'quiz_post': get_object_or_404(Post, slug=slug),
#         'cata': Catagories.objects.all().annotate(posts_count=Count('post'))
#     }
#     return render(request, template_name, post)



# # def view_404(request, Exception):
# #     content = {
# #         'title': 'Page no found'
# #     }
# #     return render(request, 'pages/error.html', content)

# # def view_500(request):
# #     content = {
# #         'title': 'Page no found'
# #     }
# #     return render(request, 'pages/error.html', content)

