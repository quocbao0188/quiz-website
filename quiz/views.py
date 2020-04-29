from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import RedirectView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Quiz, Question, Answer, Transcript, CategoryQuiz
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
    transcript_test = Transcript.objects.filter(user=request.user, quiz_item=quiz.id)
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

    if not transcript_test.exists():
        # Tao bang diem
        if request.method == 'POST':
            for z in que:
                answers = Answer.objects.filter(question_id=z.id)
                for answer in answers:
                    if answer.is_correct is True:
                        list_answer.append(answer.id)
                    else:
                        pass
                choice_id = request.POST.get('choice-' + str(z.id))
                # Ép kiểu NoneType
                if choice_id is None:
                    choice_id = "0"
                attempted_list.append(choice_id)

            # Ép kiểu String to Int và đưa vào list
            results = list(map(int, attempted_list))
            same_values = set(list_answer) & set(results)  # so sanh
            totail_correct = len(same_values)
            point = totail_correct/questions_count
            percent_correct = point*10
            print(percent_correct)
            Transcript.objects.create(
                user=request.user,
                quiz_item_id=quiz.id,
                total_score=percent_correct,
                answer_correct=totail_correct,
                question_number=questions_count)
            context = {
                'questions_count': questions_count,
                'totail_correct': totail_correct,
                'score': percent_correct,
                'quiz': quiz
            }
            return render(request, 'quiz/quiz-result.html', context)
        else:
            pass
    else:
        trans = Transcript.objects.get(user=request.user, quiz_item=quiz.id)
        if request.method == 'POST':
            for z in que:
                answers = Answer.objects.filter(question_id=z.id)
                for answer in answers:
                    if answer.is_correct is True:
                        list_answer.append(answer.id)
                    else:
                        pass
                choice_id = request.POST.get('choice-' + str(z.id))
                # Ép kiểu NoneType
                if choice_id is None:
                    choice_id = "0"
                attempted_list.append(choice_id)

            # Ép kiểu String to Int và đưa vào list
            results = list(map(int, attempted_list))
            same_values = set(list_answer) & set(results)  # so sanh
            totail_correct = len(same_values)
            point = totail_correct/questions_count
            percent_correct = point*10
            print(percent_correct)
            trans.total_score = percent_correct
            trans.answer_correct = totail_correct
            trans.question_number = questions_count
            trans.save()
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

@login_required
def transcript_show(request):
    template_name = 'quiz/transcript.html'
    take_trans = Transcript.objects.filter(user=request.user)
    post = {
        'obj': take_trans
    }
    return render(request, template_name, post)

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
