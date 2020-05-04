from django.contrib import admin
import nested_admin
from .models import Question, Quiz, Transcript, Answer, CategoryQuiz
from tinymce.widgets import TinyMCE
from django.db import models

admin.site.site_header = 'HUSHARE Administrator'

class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 4
    max_num = 4

class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [AnswerInline,]
    extra = 1

class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline,]
    list_display = ['title', 'category_quiz', 'time', 'created', 'publish']
    search_fields = ['title']
    date_hierarchy = 'created'
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

class TranscriptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz_item', 'total_score', 'transcript_date']
    search_fields = ['user__username']
    date_hierarchy = 'transcript_date'

class CategoryQuizAdmin(admin.ModelAdmin):
    fields = ['title']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(CategoryQuiz, CategoryQuizAdmin)
admin.site.register(Transcript, TranscriptAdmin)