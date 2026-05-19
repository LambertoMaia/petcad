from django.contrib import admin
from .models import Tutor, Animal


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
