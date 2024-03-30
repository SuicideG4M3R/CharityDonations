from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        min_length=8,
        max_length=128,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(
        min_length=8,
        max_length=128,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Powtórz hasło'}))


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Hasło'}))
