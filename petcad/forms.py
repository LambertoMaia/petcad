from django import forms
from django.core.exceptions import ValidationError

from .models import Tutor, Animal
from .utils import format_cep, format_cpf, format_phone, strip_digits


class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = [
            'name', 'cpf', 'email', 'telephone', 'cep',
            'street', 'number', 'complement', 'neighborhood', 'city', 'state',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: May Vitória',
                'id': 'tutor-nome',
            }),
            'cpf': forms.TextInput(attrs={
                'placeholder': '000.000.000-00',
                'id': 'tutor-cpf',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'exemplo@email.com',
                'id': 'tutor-email',
            }),
            'telephone': forms.TextInput(attrs={
                'placeholder': '(00) 00000-0000',
                'id': 'tutor-telefone',
            }),
            'cep': forms.TextInput(attrs={
                'placeholder': '00000-000',
                'id': 'tutor-cep',
            }),
            'street': forms.TextInput(attrs={
                'placeholder': 'Rua, Avenida, Travessa...',
                'id': 'tutor-logradouro',
            }),
            'number': forms.TextInput(attrs={
                'placeholder': 'Ex: 123',
                'id': 'tutor-numero',
            }),
            'complement': forms.TextInput(attrs={
                'placeholder': 'Apto, Bloco...',
                'id': 'tutor-complemento',
            }),
            'neighborhood': forms.TextInput(attrs={
                'placeholder': 'Ex: Boa Viagem',
                'id': 'tutor-bairro',
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Ex: Recife',
                'id': 'tutor-cidade',
            }),
            'state': forms.TextInput(attrs={
                'placeholder': 'Ex: PE',
                'maxlength': '2',
                'id': 'tutor-estado',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['complement'].required = False

        if self.instance and self.instance.pk:
            self.initial['cpf'] = format_cpf(self.instance.cpf)
            self.initial['telephone'] = format_phone(self.instance.telephone)
            self.initial['cep'] = format_cep(self.instance.cep)

    def clean_cpf(self):
        cpf = format_cpf(strip_digits(self.cleaned_data.get('cpf', '')))
        if len(strip_digits(cpf)) != 11:
            raise ValidationError('Informe um CPF válido com 11 dígitos.')
        qs = Tutor.objects.filter(cpf=cpf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Este CPF já está cadastrado.')
        return cpf

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = Tutor.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean_telephone(self):
        digits = strip_digits(self.cleaned_data.get('telephone', ''))
        if len(digits) not in (10, 11):
            raise ValidationError('Informe um telefone válido com DDD.')
        return format_phone(digits)

    def clean_cep(self):
        cep = format_cep(strip_digits(self.cleaned_data.get('cep', '')))
        if len(strip_digits(cep)) != 8:
            raise ValidationError('Informe um CEP válido com 8 dígitos.')
        return cep

    def clean_state(self):
        state = self.cleaned_data.get('state', '').strip().upper()
        if len(state) != 2:
            raise ValidationError('Informe a sigla do estado com 2 letras.')
        return state


class PetForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'species', 'race', 'age', 'gender', 'observations', 'owner']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Theo',
                'id': 'pet-nome',
            }),
            'species': forms.TextInput(attrs={
                'placeholder': 'Cão, Gato, Pássaro...',
                'id': 'pet-especie',
            }),
            'race': forms.TextInput(attrs={
                'placeholder': 'Ex: SRD',
                'id': 'pet-raca',
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Ex: 3',
                'id': 'pet-idade',
                'min': '0',
            }),
            'gender': forms.Select(attrs={'id': 'pet-sexo'}),
            'observations': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Informações adicionais...',
                'id': 'pet-observacoes',
            }),
            'owner': forms.Select(attrs={'id': 'pet-tutor-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['race'].required = False
        self.fields['age'].required = False
        self.fields['observations'].required = False
        self.fields['owner'].queryset = Tutor.objects.order_by('name')
        self.fields['owner'].empty_label = 'Selecione um tutor cadastrado...'
        self.fields['owner'].error_messages = {'required': 'Selecione um tutor cadastrado.'}
        self.fields['gender'].choices = [('', 'Selecione...')] + list(Animal.Gender.choices)
        self.fields['gender'].error_messages = {'required': 'Selecione o sexo do pet.'}

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age > 50:
            raise ValidationError('Informe uma idade válida (máx. 50 anos).')
        return age
