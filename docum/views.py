from django.shortcuts import render
from quiz.models import Post
# Create your views here.
def doc(request):
    content = {
        'title': 'Document',
        'doc':  Post.objects.all().order_by('-date_posted')
    }
    return render(request, 'pages/documents.html', content)