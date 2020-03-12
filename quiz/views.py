from django.shortcuts import render
from .models import Post
# Create your views here.

def index(request):
    content = {
        'title': 'Home',
        'doc':  Post.objects.all().order_by('-date_posted')
    }
    return render(request, 'pages/index.html', content)

def quiz(request, id):
    post = {
        'quiz_post': Post.objects.get(id=id)
    }
    return render(request, 'pages/quiz.html', post)

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

