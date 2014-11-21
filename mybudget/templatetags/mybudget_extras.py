# -*- coding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma


register = template.Library()


@register.filter(name='currency')
def currency(value):
    value = round(float(value), 2)
    return "%s%s" % (intcomma(int(value)), ("%0.2f" % value)[-3:].replace('.', ','))


@register.filter(name='max_length_string')
def max_length_string(value, max_length=20):
    if len(value) > max_length:
        subs = value[:max_length-4]
        return subs + ' ...'
        # TODO: why does this not work?
        # return '{} ...'.format(subs)
    return value
