# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class QuestionType(models.Model):
    """
    question type.
    for all user types.
    """

    class Meta:
        db_table = 'matching_question_type'

    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class QuestionGroup(models.Model):
    """
    question group.
    """

    class Meta:
        db_table = 'matching_question_group'

    user_type = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class QuestionSubGroup(models.Model):
    """
    question sub-group.
    """

    class Meta:
        db_table = 'matching_question_sub_group'

    question_group = models.ForeignKey(QuestionGroup)
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class QuestionScreen(models.Model):
    """
    question screen.
    """

    class Meta:
        db_table = 'matching_question_screen'

    user_type = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class QuestionSubScreen(models.Model):
    """
    question sub-screen.
    """

    class Meta:
        db_table = 'matching_question_sub_screen'

    question_screen = models.ForeignKey(QuestionScreen)
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    """
    question.
    """

    user_type = models.PositiveSmallIntegerField()
    question_group = models.ForeignKey(QuestionGroup)
    question_sub_group = models.ForeignKey(QuestionSubGroup)
    question_screen = models.ForeignKey(QuestionScreen)
    question_sub_screen = models.ForeignKey(QuestionSubScreen)
    question_type = models.ForeignKey(QuestionType)
    order_in_sub_screen = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title


class QuestionOfAnswerChoice(models.Model):
    """
    question of answer choice.
    some choices for a user to answer a question.
    """

    class Meta:
        db_table = 'matching_question_of_answer_choice'

    question = models.ForeignKey(Question)
    order = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title


class AnswerChoice(models.Model):
    """
    answer choice.
    user gives answer choice(s) for a question.
    """

    class Meta:
        db_table = 'matching_answer_choice'

    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    date_answered = models.DateTimeField()  # date last answered
    answer = models.ForeignKey(QuestionOfAnswerChoice)  # user can re-choice to answer


class AnswerText(models.Model):
    """
    answer text.
    user gives text answer(s) for a question.
    """

    class Meta:
        db_table = 'matching_answer_text'

    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    date_answered = models.DateTimeField()
    order = models.PositiveSmallIntegerField(default=0)
    answer = models.CharField(max_length=256)

    def __unicode__(self):
        return self.answer


class AnswerNumber(models.Model):
    """
    answer number.
    user gives number answer(s) for a question.
    """

    class Meta:
        db_table = 'matching_answer_number'

    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    date_answered = models.DateTimeField()
    order = models.PositiveSmallIntegerField(default=0)
    answer = models.IntegerField()


class AnswerUpload(models.Model):
    """
    answer upload.
    user upload file(s) for a question.
    """
    
    class Meta:
        db_table = 'matching_answer_upload'

    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    date_uploaded = models.DateTimeField()
    date_answered = models.DateTimeField()  # date user last edit title
    order = models.PositiveSmallIntegerField(default=0)
    size = models.PositiveIntegerField()

    # this field value pattern: md5(user_id+question_id+date_uploaded+size+file_ext_name+title)+random(10,99)
    # saving path pattern: upload/file/dir/yyyy/mm/dd/<file_name+yyyymmddhhiissxxxxxx>
    file_name = models.CharField(max_length=34)

    # for downloading file name: title.file_ext_name
    file_ext_name = models.CharField(max_length=4)

    title = models.CharField(max_length=256)  # user can edit it

    def __unicode__(self):
        return self.title