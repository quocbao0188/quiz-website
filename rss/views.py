from django.shortcuts import render
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
import feedparser
# Create your views here.
def post_detail(request, slug):
    template_name = 'rss/post-detail.html'
    post = get_object_or_404(Post, slug=slug)
    return render(request, template_name, {'post': post})

def read_rss(request):
    template_name = 'rss/read-rss.html'
    # reader = feedparser.entries('http://127.0.0.1:8000/feed/rss/')
    return render(request, template_name, {'reader': reader})