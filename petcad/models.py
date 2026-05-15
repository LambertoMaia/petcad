from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person_profile', null=True, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14) # Standard CPF length
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    animals_notes = models.TextField(blank=True, null=True) # From 'animals bigtext'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Animal(models.Model):
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=100)
    race = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.IntegerField() # e.g., 0 for Male, 1 for Female
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='animals')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.species})"
