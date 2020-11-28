from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.urls import reverse

class LatestPostsFeed(Feed):
    title = "My News"
    link = ""
    description = "New posts of my news."

    def items(self):
        return Post.objects.filter(status=1)

    def items_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)