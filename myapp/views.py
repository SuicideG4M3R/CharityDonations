from datetime import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.utils import ProgrammingError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm, LoginForm
from .models import Donation, Institution, Category
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
        user = request.user
        if not user.is_authenticated:
            return redirect('Login')
        context = {'categories': Category.objects.all() if Category.objects.count() > 0 else None,
                   'institutions': Institution.objects.all() if Institution.objects.count() > 0 else None,
                   }
        return render(request, 'form.html', context)

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect('Login')

        quantity = request.POST.get('bags')
        categories_ids = request.POST.getlist('categories')
        institution_id = request.POST.get('organization')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date_str = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')

        try:
            pick_up_date = datetime.strptime(pick_up_date_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse(f'Error daty: {pick_up_date_str}')
        print(quantity, categories_ids, institution_id, address, city, zip_code, pick_up_date, pick_up_time,
              pick_up_comment)
        donation = Donation.objects.create(
            quantity=quantity,
            institution_id=institution_id,
            address=address,
            city=city,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user,
        )
        donation.categories.set(categories_ids)
        return redirect('confirmation')


class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('Login')
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


class ConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')
