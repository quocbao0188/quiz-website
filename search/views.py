from django.shortcuts import render
from docum.models import Document
from django.db.models import Q

def search_docs(request):
    template_name = 'search/search.html'
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(title__icontains=query)|Q(content__icontains=query)|Q(species__icontains=query)
            results = Document.objects.filter(lookups).distinct()
            content = {
                'results': results,
                'submitbutton': submitbutton
            }
            return render(request, template_name, content)
        else:
            return render(request, template_name)
    else:
        return render(request, template_name)