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
# from django.db.models import Q

def quiz_list(request):
    template_name = 'quiz/quiz.html'
    quiz = Quiz.objects.filter(publish=True).annotate(question_count=Count('questions'))
    context = {
        'quiz': quiz,
        'catania': CategoryQuiz.objects.all(),
        'mosque': Quiz.objects.order_by('-create_at').filter(publish=True)[:5],
    }
    return render(request, template_name, context)


def pre_quiz(request, slug=None):
    template_name = 'quiz/pre-detail.html'
    quiz = get_object_or_404(Quiz, slug=slug, publish=True)
    question_count = Question.objects.filter(quiz_id=quiz.id).count()
    context = {
        'quiz': quiz,
        'question_count': question_count,
        'catania': CategoryQuiz.objects.all(),
        'mosque': Quiz.objects.order_by('-create_at').filter(publish=True)[:5],
    }
    return render(request, template_name, context)


@login_required
def quiz_detail(request, slug=None):
    list_answer = []
    attempted_list = []
    # Create lists containing questions to send to html
    questions = []
    not_done = []
    global user_attempted
    template_name = 'quiz/quiz-detail.html'
    # Get the selected quiz
    quiz = get_object_or_404(Quiz, slug=slug, publish=True)
    que = Question.objects.filter(quiz_id=quiz.id)
    transcript_test = Transcript.objects.filter(user=request.user, quiz_item=quiz.id)
    questions_count = que.count()

    for q in que:
        ans = Answer.objects.filter(question_id=q.id)
        question = {
            'label': q.label,
            'aidi': q.id,
            'answer': ans
        }
        questions.append(question)

        if request.method == 'POST':
            for z in que:
                answers = Answer.objects.filter(question_id=z.id)
                for answer in answers:
                    if answer.is_correct is True:
                        list_answer.append(answer.id)
                    else:
                        pass
                choice_id = request.POST.get('choice-' + str(z.id))
                # Type conversion NoneType
                if choice_id is None:
                    choice_id = "0"
                    not_done.append(choice_id)
                attempted_list.append(choice_id)

            # Type conversion from string to Int and put it into list
            results = list(map(int, attempted_list))
            print(results)
            user_attempted = results
            # Compare
            same_values = set(list_answer) & set(results)
            print(list_answer)
            print(same_values)
            total_correct = len(same_values)
            point = total_correct/questions_count
            total_not_done = len(not_done)
            print(not_done)
            print(total_not_done)
            percent_correct = point*10
            print(percent_correct)
            wrong_answer = (questions_count-total_not_done)-total_correct
            if not transcript_test.exists():
                Transcript.objects.create(
                    user=request.user,
                    quiz_item_id=quiz.id,
                    total_score=percent_correct,
                    answer_correct=total_correct,
                    unanswered=total_not_done,
                    wrong_answer=wrong_answer,
                    question_number=questions_count)
            else:
                trans = Transcript.objects.get(user=request.user, quiz_item=quiz.id)
                trans.total_score = percent_correct
                trans.answer_correct = total_correct
                trans.unanswered = total_not_done
                trans.wrong_answer = wrong_answer
                trans.question_number = questions_count
                trans.save()
            context = {
                'questions_count': questions_count,
                'total_correct': total_correct,
                'wrong_answer': wrong_answer,
                'total_not_done': total_not_done,
                'score': percent_correct,
                'quiz': quiz
            }
            return render(request, 'quiz/quiz-result.html', context)
    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, template_name, context)

@login_required
def see_answer(request, slug=None):
    questions = []
    template_name = 'quiz/quiz-answer.html'
    quiz = get_object_or_404(Quiz, slug=slug, publish=True)
    que = Question.objects.filter(quiz_id=quiz.id)
    questions_count = que.count()

    for q in que:
        ans = Answer.objects.filter(question_id=q.id)
        question = {
            'label': q.label,
            'aidi': q.id,
            'answer': ans
        }
        questions.append(question)

    context = {
        'quiz': quiz,
        'questions': questions,
        'user_attempted': user_attempted
    }
    print(user_attempted)
    return render(request, template_name, context)

@login_required
def transcript_show(request):
    template_name = 'quiz/transcript.html'
    take_trans = Transcript.objects.filter(user=request.user)
    post = {
        'obj': take_trans
    }
    return render(request, template_name, post)

@login_required
def del_transcript(request, id=None):
    trans = get_object_or_404(Transcript, id=id)
    trans.delete()
    return redirect('transcript')
# ---------------------------------------------------------------------------
def transcript_detail(request, slug=None):
    questions = []
    template_name = 'quiz/transcript-detail.html'
    quiz = get_object_or_404(Quiz, slug=slug, publish=True)
    que = Question.objects.filter(quiz_id=quiz.id)
    take_trans = get_object_or_404(Transcript, user=request.user, quiz_item=quiz)

    for q in que:
        ans = Answer.objects.filter(question_id=q.id)
        question = {
            'label': q.label,
            'aidi': q.id,
            'answer': ans
        }
        questions.append(question)

    post = {
        'obj': take_trans,
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, template_name, post)

def catago_quiz(request, slug=None):
    template_name = 'quiz/catagories-detail.html'
    catago = get_object_or_404(CategoryQuiz, slug=slug)
    list_quiz = catago.quizs.filter(publish=True).annotate(question_count=Count('questions'))
    content = {
        'catago': catago,
        'list_quiz': list_quiz,
        'catania': CategoryQuiz.objects.all(),
        'mosque': Quiz.objects.order_by('-create_at').filter(publish=True)[:5],
    }
    return render(request, template_name, content)

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
