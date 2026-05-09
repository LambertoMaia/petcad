from django.contrib import admin
from .models import Person, Animal

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'email', 'telephone')
    search_fields = ('name', 'cpf')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'race', 'owner')
    list_filter = ('species', 'gender')
    search_fields = ('name', 'owner__name')
