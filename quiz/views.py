from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import RedirectView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Quiz, Question, Answer, QuizProfile, AttemptedQuestion, CategoryQuiz
from django.contrib.auth.decorators import login_required


def quiz_list(request):
    template_name = 'quiz/quiz.html'
    quiz = Quiz.objects.all().annotate(question_count=Count('questions'))
    context = {
        'quiz': quiz,
        'cata': CategoryQuiz.objects.all().annotate(docs_count=Count('quizs'))[:5],
        'most': Quiz.objects.order_by('-created').all()[:5],
    }
    return render(request, template_name, context)


def pre_quiz(request, slug=None):
    template_name = 'quiz/pre-detail.html'
    quiz = get_object_or_404(Quiz, slug=slug)
    question_count = Question.objects.filter(quiz_id=quiz.id).count()
    context = {
        'quiz': quiz,
        'question_count': question_count
        # 'cata': CategoryQuiz.objects.all().annotate(docs_count=Count('quizs'))[:5],
        # 'most': Quiz.objects.order_by('-created').all()[:5],
    }
    return render(request, template_name, context)


@login_required
def quiz_detail(request, slug=None):
    list_answer = []
    attempted_list = []
    questions = []  # Tạo list chứa các câu hỏi để gởi xuống html
    template_name = 'quiz/quiz-detail.html'
    quiz = get_object_or_404(Quiz, slug=slug)   # Lấy cuộc thi được chọn
    # Chọn những câu hỏi trong kì thi
    que = Question.objects.filter(quiz_id=quiz.id)
    questions_count = que.count()

    for q in que:
        # Chọn bộ những câu trả lời thuộc câu hỏi
        ans = Answer.objects.filter(question_id=q.id)
        question = {
            'label': q.label,
            'aidi': q.id,
            'answer': ans
        }
        questions.append(question)

    # quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        for z in que:
            answers = Answer.objects.filter(question_id=z.id)
            for answer in answers:
                if answer.is_correct is True:
                    list_answer.append(answer.id)
                else:
                    pass

            # question_id = request.GET.get('question-' + str(z.id))
            choise_id = request.POST.get('choise-' + str(z.id))
            # Ép kiểu NoneType
            if choise_id is None:
                choise_id = "0"

            attempted_list.append(choise_id)

        # Ép kiểu String to Int và đưa vào list
        results = list(map(int, attempted_list))
        same_values = set(list_answer) & set(results)  # so sanh
        totail_correct = len(same_values)
        point = totail_correct/questions_count
        percent_correct = point*10
        print(percent_correct)
        context = {
            'questions_count': questions_count,
            'totail_correct': totail_correct,
            'score': percent_correct,
            'quiz': quiz
        }
        return render(request, 'quiz/quiz-result.html', context)
    else:
        pass
    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, template_name, context)


def see_answer(request, slug=None):
    questions = []  # Tạo list chứa các câu hỏi để gởi xuống html
    template_name = 'quiz/quiz-answer.html'
    quiz = get_object_or_404(Quiz, slug=slug)   # Lấy cuộc thi được chọn
    # Chọn những câu hỏi trong kì thi
    que = Question.objects.filter(quiz_id=quiz.id)
    questions_count = que.count()

    for q in que:
        # Chọn bộ những câu trả lời thuộc câu hỏi
        ans = Answer.objects.filter(question_id=q.id)
        question = {
            'label': q.label,
            'aidi': q.id,
            'answer': ans
        }
        questions.append(question)

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
