from django.db import models


class Tutor(models.Model):
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    cep = models.CharField(max_length=9, blank=True, default='')
    street = models.CharField(max_length=255, blank=True, default='')
    number = models.CharField(max_length=20, blank=True, default='')
    complement = models.CharField(max_length=100, blank=True, default='')
    neighborhood = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=2, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'petcad_person'

    @property
    def formatted_address(self):
        if not self.street:
            return ''
        base = f'{self.street}, {self.number}'
        if self.complement:
            base += f' — {self.complement}'
        return f'{base} — {self.city}/{self.state}'

    def __str__(self):
        return self.name


class Animal(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 0, 'Macho'
        FEMALE = 1, 'Fêmea'

    name = models.CharField(max_length=255)
    species = models.CharField(max_length=100)
    race = models.CharField(max_length=100, blank=True, default='')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.IntegerField(choices=Gender.choices)
    observations = models.TextField(blank=True, default='')
    owner = models.ForeignKey(Tutor, on_delete=models.PROTECT, related_name='animals')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_gender_display_label(self):
        return self.Gender(self.gender).label

    def __str__(self):
        return f'{self.name} ({self.species})'
