from django import forms
from django.contrib.auth import authenticate


class SignInForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=75, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'required': True,
        'tabindex': 1,
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': True,
        'tabindex': 2,
    }))

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(SignInForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        clean email, password and authenticate it.
        @return User
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        # self.check_for_test_cookie()
        return self.cleaned_data


class SignUpForm(forms.Form):
    account_type = forms.NumberInput()
    email = forms.EmailInput()
    password = forms.PasswordInput()

    def clean_account_type(self):
        account_type = self.cleaned_data['account_type']
        if account_type not in (1, 2, 3, 4):
            raise forms.ValidationError('Invalid account type')
        return account_type
