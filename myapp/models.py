from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):
    TYPE_CHOICES = [
        ('fundacja', 'Fundacja'),
        ('organizacja_pozarzadowa', 'Organizacja pozarządowa'),
        ('zbiorka_lokalna', 'Zbiórka lokalna'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=256)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='fundacja')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f'Donation ID:{self.id}'
