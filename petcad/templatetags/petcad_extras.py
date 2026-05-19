from django import template

from petcad.utils import format_cep, format_cpf, format_phone

register = template.Library()


@register.filter
def cpf_format(value):
    return format_cpf(value)


@register.filter
def phone_format(value):
    return format_phone(value)


@register.filter
def cep_format(value):
    return format_cep(value)
