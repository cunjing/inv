from django import forms


class SignupForm(forms.Form):
    account_type = forms.NumberInput()
    email = forms.EmailInput()
    password = forms.PasswordInput()

    def clean_account_type(self):
        account_type = self.cleaned_data['account_type']
        if account_type not in (1, 2, 3, 4):
            raise forms.ValidationError('Invalid account type')
        return account_type
