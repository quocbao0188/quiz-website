from django.contrib import admin
import nested_admin
from .models import Question, Quiz, Transcript, Answer, CategoryQuiz
from tinymce.widgets import TinyMCE
from django.db import models

admin.site.site_header = 'HUSHARE Administrator'

# class MultiDBModelAdmin(nested_admin.NestedModelAdmin):
#     # A handy constant for the name of the alternate database.
#     using = 'postgresql'

#     def save_model(self, request, obj, form, change):
#         # Tell Django to save objects to the 'other' database.
#         obj.save(using=self.using)

#     def delete_model(self, request, obj):
#         # Tell Django to delete objects from the 'other' database
#         obj.delete(using=self.using)

#     def get_queryset(self, request):
#         # Tell Django to look for objects on the 'other' database.
#         return super().get_queryset(request).using(self.using)

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         # Tell Django to populate ForeignKey widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         # Tell Django to populate ManyToMany widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

# class MultiDBTabularInline(nested_admin.NestedTabularInline):
#     using = 'postgresql'

#     def get_queryset(self, request):
#         # Tell Django to look for inline objects on the 'other' database.
#         return super().get_queryset(request).using(self.using)

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         # Tell Django to populate ForeignKey widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         # Tell Django to populate ManyToMany widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

# class AnswerInline(MultiDBTabularInline):
#     model = Answer
#     extra = 4
#     max_num = 4

# class QuestionInline(MultiDBTabularInline):
#     model = Question
#     inlines = [AnswerInline,]
#     extra = 1
    
#     formfield_overrides = {
#         models.TextField: {'widget': TinyMCE()},
#         }

# class QuizAdmin(MultiDBModelAdmin):
#     inlines = [QuestionInline,]
#     list_display = ['title', 'category_quiz', 'time', 'create_at', 'updated_at', 'publish']
#     search_fields = ['title']
#     date_hierarchy = 'create_at'
#     actions = ['make_published', 'make_draft']

#     fieldsets = [
#         ("Title/Category", {'fields': ["title", "category_quiz", "publish"]}),
#         ("Content/Image", {'fields': ["description", "image"]}),
#         ("Test time", {'fields': ["time"]}),
#     ]

#     formfield_overrides = {
#         models.TextField: {'widget': TinyMCE()},
#         }

#     def make_published(self, request, queryset):
#         queryset.update(publish=True)
#     make_published.short_description = "Mark selected quizzes as published"

#     def make_draft(self, request, queryset):
#         queryset.update(publish=False)
#     make_draft.short_description = "Mark selected quizzes as draft"

# class TranscriptAdmin(MultiDBModelAdmin):
#     list_display = ['user', 'quiz_item', 'total_score', 'create_at', 'updated_at']
#     search_fields = ['user__username']
#     date_hierarchy = 'create_at'

# class CategoryQuizAdmin(MultiDBModelAdmin):
#     fields = ['title']

# admin.site.register(Quiz, QuizAdmin)
# admin.site.register(CategoryQuiz, CategoryQuizAdmin)
# admin.site.register(Transcript, TranscriptAdmin)

class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 4
    max_num = 4

class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [AnswerInline,]
    extra = 1
    
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }

class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline,]
    list_display = ['title', 'author', 'slug', 'category_quiz', 'time', 'create_at', 'updated_at', 'publish']
    search_fields = ['title']
    date_hierarchy = 'create_at'
    actions = ['make_published', 'make_draft']

    fieldsets = [
        ("Title/Category", {'fields': ["title", "category_quiz", "publish"]}),
        ("Content/Image", {'fields': ["description", "image"]}),
        ("Test time", {'fields': ["time"]}),
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

class TranscriptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz_item', 'total_score', 'create_at', 'updated_at']
    search_fields = ['user__username']
    date_hierarchy = 'create_at'

class CategoryQuizAdmin(admin.ModelAdmin):
    fields = ['title']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(CategoryQuiz, CategoryQuizAdmin)
admin.site.register(Transcript, TranscriptAdmin)