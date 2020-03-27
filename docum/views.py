from django.shortcuts import render
from quiz.models import Post

# Create your views here.
def doc(request):
    template_name = 'pages/documents.html'
    return render(request, template_name)
