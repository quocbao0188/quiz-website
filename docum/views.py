from django.shortcuts import render, get_object_or_404, redirect
from .models import Document, Docatago
from django.http import HttpResponse
from django.views.generic import RedirectView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.db.models import Count
# Create your views here.

# List Document
def document_list(request):
    template_name = 'docum/documents.html'
    post = {
        'doc': Document.objects.all()
    }
    return render(request, template_name, post)

def document_detail(request, slug=None):
    template_name = 'docum/document-detail.html'
    post = {
        'doc': get_object_or_404(Document, slug=slug),
        'cata': Docatago.objects.all().annotate(docs_count=Count('document'))[:5],
        'most': Document.objects.order_by('-date_posted').all()[:5],
    }
    return render(request, template_name, post)