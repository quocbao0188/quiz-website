from django.contrib import admin
from .models import Document, Category, Order
# Register your models here.

class DocAdmin(admin.ModelAdmin):
    model = Document
    list_display = ['title', 'date_posted', 'author']
    search_fields = ['title']
    date_hierarchy = 'date_posted'


admin.site.register(Document, DocAdmin)

admin.site.register(Category)

admin.site.register(Order)