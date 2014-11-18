from django import template
from django.contrib.humanize.templatetags.humanize import intcomma


register = template.Library()


@register.filter(name='currency')
def currency(value):
    value = round(float(value), 2)
    return "%s%s" % (intcomma(int(value)), ("%0.2f" % value)[-3:].replace('.', ','))
