from django.contrib import admin
from .models import Document, Category, Order, Comment
# Register your models here.

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1
class DocAdmin(admin.ModelAdmin):
    model = Document
    list_display = ['title', 'date_posted', 'author']
    search_fields = ['title']
    date_hierarchy = 'date_posted'
    inlines = [CommentInLine]

admin.site.register(Document, DocAdmin)

admin.site.register(Category)

admin.site.register(Order)