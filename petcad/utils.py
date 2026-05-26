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


VACCINE_STATUS_CURRENT = 'current'
VACCINE_STATUS_EXPIRED = 'expired'
VACCINE_STATUS_MISSING = 'missing'

VACCINE_STATUS_LABELS = {
    VACCINE_STATUS_CURRENT: 'Em dia',
    VACCINE_STATUS_EXPIRED: 'Vencida',
    VACCINE_STATUS_MISSING: 'Em falta',
}

COMMON_VACCINES = {
    'dog': ['Antirrábica', 'Polivalente V10', 'Gripe Canina', 'Giárdia'],
    'cat': ['Antirrábica', 'Tríplice Felina', 'Leucose Felina'],
}


def get_species_group(species):
    normalized = (species or '').lower()
    if 'cão' in normalized or 'cao' in normalized:
        return 'dog'
    if 'gato' in normalized:
        return 'cat'
    return None


def get_species_emoji(species):
    group = get_species_group(species)
    if group == 'dog':
        return '🐶'
    if group == 'cat':
        return '🐱'
    return '🐾'


def vaccination_status(record, today=None):
    from django.utils import timezone

    if record is None:
        return VACCINE_STATUS_MISSING
    today = today or timezone.localdate()
    if record.next_dose_date is None:
        return VACCINE_STATUS_CURRENT
    if record.next_dose_date >= today:
        return VACCINE_STATUS_CURRENT
    return VACCINE_STATUS_EXPIRED


def get_latest_vaccinations(animal):
    latest = {}
    for vaccination in animal.vaccinations.all():
        key = vaccination.name.strip().lower()
        if key not in latest:
            latest[key] = vaccination
    return latest


def build_vaccination_overview(animal, today=None):
    from django.utils import timezone

    today = today or timezone.localdate()
    catalog = COMMON_VACCINES.get(get_species_group(animal.species), [])
    latest = get_latest_vaccinations(animal)
    rows = []
    counts = {
        VACCINE_STATUS_CURRENT: 0,
        VACCINE_STATUS_EXPIRED: 0,
        VACCINE_STATUS_MISSING: 0,
    }

    if catalog:
        for name in catalog:
            record = latest.get(name.lower())
            status = vaccination_status(record, today)
            counts[status] += 1
            rows.append({
                'name': name,
                'record': record,
                'status': status,
                'status_label': VACCINE_STATUS_LABELS[status],
            })
    else:
        for record in animal.vaccinations.all():
            status = vaccination_status(record, today)
            counts[status] += 1
            rows.append({
                'name': record.name,
                'record': record,
                'status': status,
                'status_label': VACCINE_STATUS_LABELS[status],
            })

    return rows, counts
