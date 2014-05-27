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

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'leader':
            kwargs['queryset'] = User.objects.filter(is_staff=0)
        return super(ProfileInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class InvUserAdmin(UserAdmin):
    inlines = [ProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, InvUserAdmin)