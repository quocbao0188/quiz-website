from django.shortcuts import render
from quiz.models import Post
# from django.views.generic import ListView
# Create your views here.

def index(request):
    template_name = 'pages/index.html'
    content = {
        'doc':  Post.objects.all()
    }
    return render(request, template_name, content)

# List View Index
# class HomeListView(ListView):
#     model = Post
#     # <app>/<model>_<viewtype>.html
#     template_name = 'pages/index.html'
#     context_object_name = 'doc'
#     paginate_by = 3