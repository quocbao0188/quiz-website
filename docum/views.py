from django.shortcuts import render, get_object_or_404, redirect
from .models import Document, Category, Order
from users.models import Profile
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import RedirectView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

# List Document
def document_list(request):
    template_name = 'docum/documents.html'
    doc_list = Document.objects.filter(species='DOC')

    page = request.GET.get('page', 1)
    paginator = Paginator(doc_list, 5)

    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)
        
    post = {
        'doc': docs,
        'cata': Category.objects.all().annotate(docs_count=Count('documents'))[:5],
        'most': Document.objects.order_by('-date_posted').all()[:5],
    }
    return render(request, template_name, post)

def lab_list(request):
    template_name = 'docum/lab.html'
    labs_list = Document.objects.filter(species='LAB')
    page = request.GET.get('page', 1)
    paginator = Paginator(labs_list, 5)

    try:
        labs = paginator.page(page)
    except PageNotAnInteger:
        labs = paginator.page(1)
    except EmptyPage:
        labs = paginator.page(paginator.num_pages)

    post = {
        'lab': labs,
        'cata': Category.objects.all().annotate(docs_count=Count('documents'))[:5],
        'most': Document.objects.order_by('-date_posted').all()[:5],
    }
    return render(request, template_name, post)

# @login_required
def document_detail(request, slug=None):
    template_name = 'docum/document-detail.html'
    doz = get_object_or_404(Document, slug=slug)
    if request.user.is_authenticated:
        order_obj = Order.objects.filter(user=request.user, items=doz.id)
    else:
        order_obj = None
    post = {
        'doc': doz,
        'ord': order_obj,#Order.objects.filter(user=request.user, items=doz.id),
        'cata': Category.objects.all().annotate(docs_count=Count('documents'))[:5],
        'most': Document.objects.order_by('-date_posted').all()[:5],
    }
    return render(request, template_name, post)

@login_required
def buy_item(request, slug=None):
    item = get_object_or_404(Document, slug=slug)
    order_qs = Order.objects.filter(user=request.user)
    user_now = Profile.objects.get(user=request.user)
    doz = Document.objects.get(slug=slug)
    print(user_now.credit)
    print(order_qs)

    if Order.objects.filter(user=request.user, items=doz.id).exists():
        messages.warning(request, f'Ban da mua')
    else:
        if user_now.credit >= doz.credit:
            if order_qs.exists():
                order = order_qs[0]
                order.items.add(item)
            else:
                order = Order.objects.create(user=request.user)
                order.items.add(item)
            user_now.credit = user_now.credit - doz.credit
            print(user_now.credit)
            user_now.save()
            messages.success(request, f'Ban da mua thanh cong')
        else:
            messages.warning(request, f'Ban khong du tien de mua tai lieu')

    return redirect('doc-detail', slug=slug)

def catago_list(request, slug=None):
    template_name = 'docum/catagories-detail.html'
    catago = get_object_or_404(Category, slug=slug)
    list_doc = catago.documents.all()
    content = {
        'catago': catago,
        'list_doc': list_doc,
        'cata': Category.objects.all().annotate(docs_count=Count('documents'))[:5],
        'most': Document.objects.order_by('-date_posted').all()[:5],
    }
    return render(request, template_name, content)

@login_required
def buy_detail(request):
    try:
        template_name = 'docum/buy-detail.html'
        post = {
            'obj': Order.objects.get(user=request.user)
        }
        return render(request, template_name, post)
    except ObjectDoesNotExist:
        messages.warning(request, f'Ban chua mua tai lieu nao')
        return redirect("/")
