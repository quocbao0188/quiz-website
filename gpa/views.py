from django.shortcuts import render

# Create your views here.

def calculator(request):
    template_name = 'gpa/gpa.html'
    return render(request, template_name)
