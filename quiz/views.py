from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.http import HttpResponse
from django.views.generic import RedirectView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
# Create your views here.

# List View Index
class QuizListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    template_name = 'pages/quiz.html'
    context_object_name = 'doc'
    paginate_by = 1

# class QuizDetailView(DetailView):
#     model = Post
#     template_name = 'pages/quiz-detail.html'

class QuizLikeRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        urls_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return urls_

class QuizLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        urls_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True

        data = {
            "updated": updated,
            "liked": liked
        }

        return Response(data)


# def quiz(request):
#     template_name = 'pages/quiz.html'
#     content = {
#         'doc':  Post.objects.all()#.order_by('-date_posted')
#     }
#     return render(request, template_name, content)

def quiz_detail(request, slug=None):
    template_name = 'pages/quiz-detail.html'
    post = {
        'quiz_post': get_object_or_404(Post, slug=slug)
    }
    return render(request, template_name, post)



def view_404(request, Exception):
    content = {
        'title': 'Page no found'
    }
    return render(request, 'pages/error.html', content)

def view_500(request):
    content = {
        'title': 'Page no found'
    }
    return render(request, 'pages/error.html', content)

