# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from models import Profile


class SignInForm(forms.Form):
    """
    sign in form
    """

    email = forms.EmailField(label='Email', min_length=4, max_length=75, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'required': True,
        'tabindex': 1,
    }))

    password = forms.CharField(label='Password', min_length=6, max_length=128, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': True,
        'tabindex': 2,
    }))

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(SignInForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SignInForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        msg = u'invalid email or password.'
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is not None:
                if not self.user_cache.is_active:
                    msg = u'your account is not active.'
                else:
                    msg = ''
        if msg:
            self._errors['submit'] = self.error_class([msg])
            if None != cleaned_data.get('email'):
                del cleaned_data['email']
            if None != cleaned_data.get('password'):
                del cleaned_data['password']

        return cleaned_data


class SignUpForm(forms.Form):
    """
    sign up form
    """

    _account_type_allowed = (
        {'key': '', 'text': 'Account Type'},
        {'key': 1, 'text': 'Investee'},
        {'key': 2, 'text': 'Investor'},
        {'key': 3, 'text': 'Service Provider'},
        {'key': 4, 'text': 'Government'},
    )
    account_type = forms.Select(choices=_account_type_allowed)

    email = forms.EmailField(label='Email', min_length=4, max_length=75, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'required': True,
        'tabindex': 2,
    }))

    password = forms.CharField(label='Password', min_length=6, max_length=128, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': True,
        'tabindex': 3,
    }))

    def clean_account_type(self):
        account_type = int(self.cleaned_data['account_type'])
        tmp = False
        for row in self._account_type_allowed:
            if account_type == row.key:
                tmp = True
                break
        if not tmp:
            raise forms.ValidationError(u'Invalid account type.')
        return account_type

    def clean_email(self):
        email = User.objects.filter(email=self.cleaned_data['email'])
        if email:
            raise forms.ValidationError(u'Email has been existed.')
        return self.cleaned_data['email']

    def create_user(self):
        """
        create user and it's profile.

        @return (User)
        """

        account_type = self.cleaned_data['account_type']
        username = email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        with transaction.atomic():
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile.objects.create(user_id=user.id, account_type=account_type)
            profile.save()

        return user
