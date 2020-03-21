from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
# Create your views here.

def index(request):
    content = {
        'title': 'Home',
        'doc':  Post.objects.all()#.order_by('-date_posted')
    }
    return render(request, 'pages/index.html', content)

# List View Index
class QuizListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    template_name = 'pages/index.html'
    context_object_name = 'doc'
    paginate_by = 3

class QuizDetailView(DetailView):
    model = Post
    template_name = 'pages/quiz-detail.html'

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

