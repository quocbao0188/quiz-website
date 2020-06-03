from django.shortcuts import render
from docum.models import Document
from quiz.models import Quiz
from django.db.models import Q

def search(request):
    template_name = 'search/search.html'
    return render(request, template_name)

def search_docs(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        type_search = request.GET.get('typeSearch')
        submitbutton = request.GET.get('submit')
        if type_search == '1':
            if query is not None:
                # &Q(species__icontains='DOC')
                lookups = Q(title__icontains=query)&Q(species__icontains='DOC')
                results = Document.objects.filter(lookups).distinct()
                content = {
                    'results': results,
                    'submitbutton': submitbutton,
                    'header': 'Documents Search'
                }
                return render(request, 'search/search-docs.html', content)
            else:
                return render(request, 'search/search-docs.html')
        elif type_search == '2':
            if query is not None:
                lookups = Q(title__icontains=query)&Q(species__icontains='LAB')
                results = Document.objects.filter(lookups).distinct()
                content = {
                    'results': results,
                    'submitbutton': submitbutton,
                    'header': 'Practice Labs Search'
                }
                return render(request, 'search/search-docs.html', content)
            else:
                return render(request, 'search/search-docs.html')
        elif type_search == '3':
            if query is not None:
                lookups = Q(title__icontains=query)|Q(category_quiz__title__icontains=query)
                results = Quiz.objects.filter(lookups).distinct()
                content = {
                    'results': results,
                    'submitbutton': submitbutton,
                    'header': 'Quizzes Search'
                }
                return render(request, 'search/search-quizzes.html', content)
            else:
                return render(request, 'search/search-quizzes.html')
        elif type_search == '4':
            if query is not None:
                lookups = Q(title__icontains=query)&Q(species__icontains='OTH')
                results = Document.objects.filter(lookups).distinct()
                content = {
                    'results': results,
                    'submitbutton': submitbutton,
                    'header': 'Other Search'
                }
                return render(request, 'search/search-docs.html', content)
            else:
                return render(request, 'search/search-docs.html')
        else:
            if query is not None:
                lookups = Q(title__icontains=query)|Q(catago__title__icontains=query)
                results = Document.objects.filter(lookups).distinct()
                content = {
                    'results': results,
                    'submitbutton': submitbutton,
                    'header': 'Document, Practice Labs and Other Search'
                }
                return render(request, 'search/search-docs.html', content)
            else:
                return render(request, 'search/search-docs.html')
    else:
        return render(request, 'search/search-quizzes.html')