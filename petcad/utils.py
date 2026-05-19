import re

from django.db.models import Q


SPECIES_FILTERS = {
    'cao': Q(species__icontains='cão') | Q(species__icontains='cao'),
    'gato': Q(species__icontains='gato'),
    'passaro': Q(species__icontains='pássaro') | Q(species__icontains='passaro'),
}


def strip_digits(value):
    return re.sub(r'\D', '', value or '')


def format_cpf(value):
    digits = strip_digits(value)[:11]
    if len(digits) != 11:
        return value
    return f'{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}'


def format_phone(value):
    digits = strip_digits(value)[:11]
    if len(digits) == 11:
        return f'({digits[:2]}) {digits[2:7]}-{digits[7:]}'
    if len(digits) == 10:
        return f'({digits[:2]}) {digits[2:6]}-{digits[6:]}'
    return value


def format_cep(value):
    digits = strip_digits(value)[:8]
    if len(digits) == 8:
        return f'{digits[:5]}-{digits[5:]}'
    return value


def filter_animals_by_species(queryset, species_key):
    if not species_key:
        return queryset
    if species_key == 'outro':
        combined = SPECIES_FILTERS['cao'] | SPECIES_FILTERS['gato'] | SPECIES_FILTERS['passaro']
        return queryset.exclude(combined)
    filter_q = SPECIES_FILTERS.get(species_key)
    if filter_q:
        return queryset.filter(filter_q)
    return queryset
