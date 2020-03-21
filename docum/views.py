from django.shortcuts import render
from django.views.generic import ListView, DetailView
from quiz.models import Post

# Create your views here.
def doc(request):
    content = {
        'title': 'Document',
        'doc':  Post.objects.all().order_by('-date_posted')
    }
    return render(request, 'pages/documents.html', content)

class DocListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    template_name = 'pages/documents.html'
    context_object_name = 'doc'

class DocDetailView(DetailView):
    model = Post