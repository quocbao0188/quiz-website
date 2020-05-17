from django.contrib import admin
from tinymce.widgets import TinyMCE
from .models import Document, Category, Order, Comment
from django.db import models
# Register your models here.

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1
class DocAdmin(admin.ModelAdmin):
    model = Document
    list_display = ['title', 'species', 'create_at', 'updated_at', 'credit']
    search_fields = ['title']
    date_hierarchy = 'create_at'
    inlines = [CommentInLine]

    fieldsets = [
        ("Title/Category", {'fields': ["title", "species", "catago"]}),
        ("Content/Image", {'fields': ["content", "image"]}),
        ("URL download", {'fields': ["link_url"]}),
        ("More setting", {'fields': ["author", "like", "credit"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }

class CategoryAdmin(admin.ModelAdmin):
    fields = ['title']

admin.site.register(Document, DocAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Order)