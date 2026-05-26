from django.contrib import admin
from .models import Tutor, Animal, Vaccination


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'email', 'telephone')
    search_fields = ('name', 'cpf', 'email')
    readonly_fields = ('created_at',)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'race', 'owner', 'gender')
    list_filter = ('species', 'gender')
    search_fields = ('name', 'owner__name')


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal', 'application_date', 'next_dose_date', 'vaccine_type')
    list_filter = ('vaccine_type', 'application_date')
    search_fields = ('name', 'animal__name')
    readonly_fields = ('created_at',)
