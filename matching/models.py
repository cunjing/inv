# -*- coding: utf-8 -*-
from django.db import models
from account.models import UserType


class QuestionType(models.Model):
    """
    question type.
    for all user types.
    """

    title = models.CharField(max_length=40)


class QuestionGroup(models.Model):
    """
    question group.
    """

    user_type_id = models.ForeignKey(UserType, db_column='user_type_id', related_name='user_type')
    title = models.CharField(max_length=40)


class QuestionSubGroup(models.Model):
    """
    question sub-group.
    """

    group_id = models.ForeignKey(QuestionGroup, db_column='group_id', related_name='group')
    title = models.CharField(max_length=40)


class QuestionScreen(models.Model):
    """
    question screen.
    """

    user_type_id = models.ForeignKey(UserType, db_column='user_type_id', related_name='user_type')
    title = models.CharField(max_length=40)


class QuestionSubScreen(models.Model):
    """
    question sub-screen.
    """

    screen_id = models.ForeignKey(QuestionScreen, db_column='screen_id', related_name='screen')
    title = models.CharField(max_length=40)


class Question(models.Model):
    """
    question.
    """

    user_type_id = models.ForeignKey(UserType, db_column='user_type_id', related_name='user_type')
    group_id = models.ForeignKey(QuestionGroup, db_column='group_id', related_name='group')
    sub_group_id = models.ForeignKey(QuestionSubGroup, db_column='sub_group_id', related_name='sub_group')
    screen_id = models.ForeignKey(QuestionScreen, db_column='screen_id', related_name='screen')
    sub_screen_id = models.ForeignKey(QuestionSubScreen, db_column='sub_screen_id', related_name='sub_screen')
    type_id = models.ForeignKey(QuestionType, db_column='type_id', related_name='type')
    order_in_sub_screen = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=256)


class QuestionOfAnswerChoice(models.Model):
    """
    question of answer choice.
    """

    question_id = models.ForeignKey(Question, db_column='question_id', related_name='question')
    order = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=256)


class Answer(models.Model):
    """
    answer.
    TODO: user gives answers for questions.
    """
    pass
