from django.contrib import admin
from .models import Post
# Register your models here.

admin.site.site_header = 'HUSHARE Administrator'

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_posted', 'author']
    search_fields = ['title']

admin.site.register(Post, PostAdmin)