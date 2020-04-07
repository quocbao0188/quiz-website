from django.contrib import admin
# Register your models here.

admin.site.site_header = 'HUSHARE Administrator'

# class PostAdmin(admin.ModelAdmin):
#     list_display = ['title', 'date_posted', 'author']
#     search_fields = ['title']
#     date_hierarchy = 'date_posted'

# admin.site.register(Post, PostAdmin)