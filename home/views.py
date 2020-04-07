from django.shortcuts import render, get_object_or_404, redirect
from docum.models import Document
# from django.views.generic import ListView
# Create your views here.

def index(request):
    template_name = 'home/index.html'
    content = {
        'doc':  Document.objects.all()
    }
    return render(request, template_name, content)

# List View Index
# class HomeListView(ListView):
#     model = Post
#     # <app>/<model>_<viewtype>.html
#     template_name = 'pages/index.html'
#     context_object_name = 'doc'
#     paginate_by = 3

def view_404(request, Exception):
    content = {
        'title': 'Page no found'
    }
    return render(request, 'error.html', content)

def view_500(request):
    content = {
        'title': 'Page no found'
    }
    return render(request, 'error.html', content)
