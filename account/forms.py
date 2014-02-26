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

    email = forms.EmailField(label='Email', max_length=75, min_length=4, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'required': True,
        'tabindex': 1,
    }))

    password = forms.CharField(label='Password', max_length=128, min_length=6, widget=forms.PasswordInput(attrs={
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

        msg = u'Invalid email or password.'
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is not None:
                if not self.user_cache.is_active:
                    msg = u'Your account is not active.'
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
        ('', 'Account Type'),
        (1, 'Investee'),
        (2, 'Investor'),
        (3, 'Service Provider'),
        (4, 'Government'),
    )

    account_type = forms.IntegerField(max_value=4, min_value=1, widget=forms.Select(attrs={
        'class': 'form-control',
        'required': True,
        'tabindex': 1,
    }, choices=_account_type_allowed))

    email = forms.EmailField(label='Email', max_length=75, min_length=4, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'required': True,
        'tabindex': 2,
    }))

    password = forms.CharField(label='Password', max_length=128, min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': True,
        'tabindex': 3,
    }))

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
            user.backend = 'account.backends.EmailAuthBackend'
            user.save()
            profile = Profile.objects.create(user_id=user, account_type=account_type)
            profile.save()

        return user
