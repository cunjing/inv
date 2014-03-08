from django.contrib import admin
from models import *


admin.site.register(QuestionType)


class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'order', 'name', 'title')
    ordering = ('id',)
admin.site.register(QuestionGroup, QuestionGroupAdmin)


class QuestionSubGroupAdmin(admin.ModelAdmin):
    list_display = ('question_group', 'order', 'name', 'title')
    ordering = ('id',)
admin.site.register(QuestionSubGroup, QuestionSubGroupAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_group', 'question_sub_group', 'question_type', 'order', 'title')
    ordering = ('id',)
admin.site.register(Question, QuestionAdmin)


class QuestionOfAnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'title')
    ordering = ('id',)
admin.site.register(QuestionOfAnswerChoice, QuestionOfAnswerChoiceAdmin)
