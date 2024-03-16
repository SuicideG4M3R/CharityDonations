from django.db.utils import ProgrammingError
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from myapp.models import Donation, Institution
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
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
