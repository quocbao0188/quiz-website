from django.shortcuts import render
from .models import Post
# Create your views here.

def index(request):
    content = {
        'title': 'Home',
        'doc':  Post.objects.all().order_by('-date_posted')
    }
    return render(request, 'pages/index.html', content)

def doc(request):
    content = {
        'title': 'Document',
        'doc':  Post.objects.all().order_by('-date_posted')
    }
    return render(request, 'pages/documents.html', content)

def quiz(request, id):
    post = {
        'quiz': Post.objects.get(id=id)
    }
    return render(request, 'pages/quiz.html', post)