# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate


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
    password = forms.CharField(label='Password', min_length=4, widget=forms.PasswordInput(attrs={
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

    account_type = forms.NumberInput()
    email = forms.EmailInput()
    password = forms.PasswordInput()

    def clean_account_type(self):
        account_type = self.cleaned_data['account_type']
        if account_type not in (1, 2, 3, 4):
            raise forms.ValidationError('Invalid account type')
        return account_type
