from django.shortcuts import render, get_object_or_404, redirect
from .models import Document, Category, Order, Comment
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
from .forms import CommentForm
from django.http import HttpResponseRedirect
# import csv

# List Document
def document_list(request):
    template_name = 'docum/documents.html'
    doc_list = Document.objects.filter(species='DOC', publish=True)

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
        'cata': Category.objects.all(),
        'most': Document.objects.order_by('-create_at').filter(species='DOC', publish=True)[:5],
    }
    return render(request, template_name, post)

def lab_list(request):
    template_name = 'docum/lab.html'
    labs_list = Document.objects.filter(species='LAB', publish=True)
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
        'cata': Category.objects.all(),
        'most': Document.objects.order_by('-create_at').filter(species='LAB', publish=True)[:5],
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

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user, document=doz)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)

    post = {
        'doc': doz,
        'ord': order_obj,
        'form': form,
        'cata': Category.objects.all(),
        'most': Document.objects.order_by('-create_at').filter(publish=True)[:5],
    }
    return render(request, template_name, post)

def delete_comment(request, id=None):
    comment = get_object_or_404(Comment, id=id)
    if comment.user == request.user:
        comment.delete()
        messages.success(request, "Successfully Deleted")
        return redirect('doc-detail')
        # return HttpResponseRedirect(request.path_info)

@login_required
def buy_item(request, slug=None):
    item = get_object_or_404(Document, slug=slug)
    order_qs = Order.objects.filter(user=request.user, items_id=item.id)
    if Profile.objects.filter(user=request.user).exists():
        user_now = Profile.objects.get(user=request.user)
        if not order_qs.exists():
            if user_now.credit >= item.credit:
                Order.objects.create(user=request.user, items_id=item.id)
                user_now.credit = user_now.credit - item.credit
                print(user_now.credit)
                user_now.save()
                messages.success(request, f'You have successfully purchased')
            else:
                messages.warning(request, f'You do not have enough money to buy documents')
        else:
            messages.warning(request, f'You have purchased before')
    else:
        messages.warning(request, f'You have to finish your Profile first !')
    # if order_qs.exists():
    #     messages.warning(request, f'You have successfully purchased')
    # else:
    #     if user_now.credit >= doz.credit:
    #         if order_qs.exists():
    #             order = order_qs[0]
    #             order.items.add(item)
    #         else:
    #             order = Order.objects.create(user=request.user)
    #             order.items.add(item)
    #         user_now.credit = user_now.credit - doz.credit
    #         print(user_now.credit)
    #         user_now.save()
    #         messages.success(request, f'You have successfully purchased')
    #     else:
    #         messages.warning(request, f'You do not have enough money to buy documents')

    return redirect('doc-detail', slug=slug)

def catago_list(request, slug=None):
    template_name = 'docum/catagories-detail.html'
    catago = get_object_or_404(Category, slug=slug)
    list_doc = catago.documents.filter(publish=True)
    content = {
        'catago': catago,
        'list_doc': list_doc,
        'cata': Category.objects.all(),
        'most': Document.objects.order_by('-create_at').filter(publish=True)[:5],
    }
    return render(request, template_name, content)

@login_required
def buy_detail(request):
    template_name = 'docum/buy-detail.html'
    post = {
        'obj': Order.objects.filter(user=request.user)
    }
    return render(request, template_name, post)


# def export_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="document.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Title', 'Slug'])

#     for docs in Document.objects.all().values_list('title', 'slug', 'species', 'catago', 'content', 'link_url', 'author', 'image', 'date_posted', 'credit'):
#         writer.writerow(docs)

#     return response