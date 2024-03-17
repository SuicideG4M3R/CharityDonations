from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.utils import ProgrammingError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm, LoginForm
from .models import Donation, Institution
from django.db.models import Sum


class LandingPageView(View):
    def get(self, request):
        try:
            total_donated_bags = Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags']
            if total_donated_bags is None:
                total_donated_bags = 0
            supported_organizations = Institution.objects.count()
            all_foundations = Institution.objects.filter(type='fundacja')
            all_organizations = Institution.objects.filter(type='organizacja_pozarzadowa')
            all_local_collections = Institution.objects.filter(type='zbiorka_lokalna')
        except ProgrammingError:
            return HttpResponse('Error: Błąd z bazą danych, views.py line 18')

        context = {
            'total_donated_bags': total_donated_bags,
            'supported_organizations': supported_organizations,

            'all_foundations': all_foundations,
            'all_organizations': all_organizations,
            'all_local_collections': all_local_collections,
        }

        return render(request, 'index.html', context)


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            if User.objects.filter(username=email).exists():
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'login.html',
                                  {'form': form,
                                   'error_message': 'Błąd logowania, podaj prawidłowy adres e-mail i hasło'})
            else:
                return redirect('Register')
        return render(request, 'login.html',
                      {'form': form,
                       'error_message': 'Wypełnij formularz poprawnie', })


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            if User.objects.filter(username=email).exists():
                return render(request, 'register.html',
                              {'form': form, 'error_message': f'{email} jest już zajęty'})
            if password != password2:
                return render(request, 'register.html',
                              {'form': form, 'error_message': 'Hasła nie pasują się'})
            if len(password) < 8:
                return render(request, 'register.html',
                              {'form': form, 'error_message': 'Hasło musi zawierać co najmniej 8 znaków'})
            try:
                user = User.objects.create_user(first_name=name, last_name=surname, username=email, password=password)
            except Exception as error:
                return render(request, 'register.html',
                              {'form': form, 'error_message': str(error)})
            login(request, user)
            return redirect('home')
        return render(request, 'register.html',
                      {'form': form, 'error_message': 'Wypełnij formularz poprawnie'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
