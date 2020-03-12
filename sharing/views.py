from django.shortcuts import render

# Create your views here.
def sharing(request):
    content = {
        'title': 'Sharing'
    }
    return render(request, 'pages/sharing.html', content)