from django.contrib import admin
from .models import Document, Docatago, Order
# Register your models here.

class DocAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_posted', 'author']
    search_fields = ['title']
    date_hierarchy = 'date_posted'

admin.site.register(Document, DocAdmin)

admin.site.register(Docatago)

admin.site.register(Order)