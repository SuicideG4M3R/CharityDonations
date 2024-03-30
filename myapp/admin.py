from django.contrib import admin
from .models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'get_categories_list')
    search_fields = ('name', 'type')
    list_filter = ('type',)

    def get_categories_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories_list.short_description = 'Categories'
