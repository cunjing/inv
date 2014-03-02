# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from account.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = 'user'
    extra = 1
    can_delete = False
    verbose_name_plural = 'profile'

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        if db_field.name == 'leader':
            kwargs['choices'][0] = (0, 'none')
        return super(ProfileInline, self).formfield_for_choice_field(db_field, request, **kwargs)


class InvUserAdmin(UserAdmin):
    inlines = [ProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, InvUserAdmin)