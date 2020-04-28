from django.contrib import admin
import nested_admin
from .models import Question, Quiz, Transcript, Answer, CategoryQuiz
# Register your models here.

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


admin.site.register(Quiz, QuizAdmin)
admin.site.register(CategoryQuiz)
admin.site.register(Transcript)