from django.contrib import admin
from models import *


admin.site.disable_action('delete_selected')


class QuestionTypeAdmin(admin.ModelAdmin):
    ordering = ('id',)

admin.site.register(QuestionType, QuestionTypeAdmin)


class QuestionGroupAdmin(admin.ModelAdmin):
    list_filter = ('user_type',)
    list_display = ('user_type', 'order', 'name', 'title')
    ordering = ('id',)
    list_display_links = ('title',)

admin.site.register(QuestionGroup, QuestionGroupAdmin)


class QuestionSubGroupAdmin(admin.ModelAdmin):
    list_display = ('question_group', 'order', 'name', 'title')
    ordering = ('id',)

admin.site.register(QuestionSubGroup, QuestionSubGroupAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_group', 'question_sub_group', 'question_type', 'order', 'title')
    ordering = ('id',)

    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     if db_field.name == 'question_sub_group':
    #         kwargs['queryset'] = QuestionSubGroup.objects.filter(question_group=self.question_group)
    #     return super(QuestionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Question, QuestionAdmin)


class QuestionOfAnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'title')
    ordering = ('id',)

admin.site.register(QuestionOfAnswerChoice, QuestionOfAnswerChoiceAdmin)
