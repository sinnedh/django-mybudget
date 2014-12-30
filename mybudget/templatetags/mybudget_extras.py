# -*- coding: utf-8 -*-
from math import modf

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma


register = template.Library()


@register.simple_tag(name='fa_icon')
def fa_icon(key, size=''):
    return '<i class="fa fa-{} {}"></i>'.format(key, size)


@register.simple_tag(name='currency')
def currency(value, currency='&euro;'):
    cents, euros= modf(value)
    return "{}<sup>{:02}</sup> {}".format(int(euros), int(cents * 100), currency)


@register.simple_tag(name='currency_simple')
def currency_simple(value, currency='&euro;'):
    euros= round(value)
    return "{} {}".format(int(euros), currency)


@register.filter(name='max_length_string')
def max_length_string(value, max_length=20):
    if len(value) > max_length:
        subs = value[:max_length-4]
        return subs + ' ...'
        # TODO: why does this not work?
        # return '{} ...'.format(subs)
    return value
