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
    list_display = ['title', 'species', 'credit', 'create_at', 'updated_at', 'publish']
    search_fields = ['title']
    date_hierarchy = 'create_at'
    inlines = [CommentInLine]
    actions = ['make_published', 'make_draft']

    fieldsets = [
        ("Title/Category", {'fields': ["title", "publish", "species", "catago"]}),
        ("Content/Image", {'fields': ["content", "image"]}),
        ("URL download", {'fields': ["link_url", "backup_link"]}),
        ("Price of material", {'fields': ["credit"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }
    
    def make_published(self, request, queryset):
        queryset.update(publish=True)
    make_published.short_description = "Mark selected quizzes as published"

    def make_draft(self, request, queryset):
        queryset.update(publish=False)
    make_draft.short_description = "Mark selected quizzes as draft"

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class CategoryAdmin(admin.ModelAdmin):
    fields = ['title']

admin.site.register(Document, DocAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Order)