from django.shortcuts import render

# Create your views here.
def sharing(request):
    template_name = 'pages/sharing.html'
    return render(request, template_name)