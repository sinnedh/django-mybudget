# -*- coding: utf-8 -*-
from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


ICONS_CHOICES = (
    ('', '--------'),
    ('ambulance', _('Ambulance')),
    ('anchor', _('Anchor')),
    ('beer', _('Beer')),
    ('bicycle', _('Bicycle')),
    ('binoculars', _('Binoculars')),
    ('book', _('Books')),
    ('briefcase', _('Briefcase')),
    ('building', _('Building')),
    ('bus', _('Bus')),
    ('calendar', _('Calendar')),
    ('camera', _('Camera')),
    ('car', _('Car')),
    ('child', _('Child')),
    ('cloud', _('Cloud')),
    ('coffee', _('Coffee')),
    ('credit-card', _('Credit card')),
    ('cutlery', _('Cutlery')),
    ('envelope', _('Envelope')),
    ('eye', _('Eye')),
    ('film', _('Film')),
    ('fire', _('Fire')),
    ('flag', _('Flag')),
    ('flash', _('Flash')),
    ('gamepad', _('Gamepad')),
    ('gift', _('Gifts')),
    ('glass', _('Glass')),
    ('globe', _('Globe')),
    ('headphones', _('Headphones')),
    ('home', _('Home')),
    ('key', _('Key')),
    ('laptop', _('Laptop')),
    ('leaf', _('Leaf')),
    ('medkit', _('Medkit')),
    ('microphone', _('Microphone')),
    ('mobile', _('Mobile')),
    ('music', _('Music')),
    ('newspaper-o', _('Newspaper')),
    ('paperclip', _('Office')),
    ('paint-brush', _('Paint brush')),
    ('paw', _('Paw')),
    ('pencil', _('Pencil')),
    ('photo', _('Photo')),
    ('phone', _('Phone')),
    ('plane', _('Plane')),
    ('plug', _('Plug')),
    ('print', _('Printer')),
    ('road', _('Road')),
    ('scissors', _('Scissors')),
    ('shopping-cart', _('Shopping')),
    ('futbol-o', _('Soccer ball')),
    ('spoon', _('Spoon')),
    ('stethoscope', _('Stethoscope')),
    ('suitcase', _('Suitcase')),
    ('support', _('Support')),
    ('sun-o', _('Sun')),
    ('taxi', _('Taxi')),
    ('tint', _('Tint')),
    ('trash', _('Trash')),
    ('tree', _('Tree')),
    ('trophy', _('Trophy')),
    ('truck', _('Truck')),
    ('umbrella', _('Umbrella')),
    ('university', _('University')),
    ('video-camera', _('Video camera')),
    ('wifi', _('Wifi')),
    ('wheelchair', _('Wheelchair')),
    ('wrench', _('Wrench')),
)


class BootstrapDateWidget(forms.widgets.DateInput):

    def render(self, name, value, attrs=None):
        attrs['data-provide'] = 'datepicker'
        html = ('<div class="input-group date">'
                '{}'
                '<span class="input-group-addon">'
                '<i class="glyphicon glyphicon-calendar"></i>'
                '</span>'
                '</div>')
        html = html.format(super(BootstrapDateWidget, self).render(name, value, attrs))
        return mark_safe(html)


class BootstrapCurrencyWidget(forms.widgets.TextInput):

    def render(self, name, value, attrs=None):
        html = ('<div class="input-group">'
                '{}'
                '<span class="input-group-addon">'
                '<i class="glyphicon glyphicon-euro"></i>'
                '</span>'
                '</div>')
        html = html.format(super(BootstrapCurrencyWidget, self).render(name, value, attrs))
        return mark_safe(html)


class IconSelectWidget(forms.widgets.Select):

    def __init__(self, attrs=None, choices=()):
        super(IconSelectWidget, self).__init__(attrs, choices)
        self.attrs['class'] = 'selectpicker'

    def get_data_icon(self, option_value):
        return option_value

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        data_icon = self.get_data_icon(option_value)
        return format_html(u'<option data-icon="fa-{0}" value="{1}"{2}>{3}</option>',
                           data_icon,
                           option_value,
                           selected_html,
                           force_text(option_label))


from models import Category


class CategorySelectWidget(IconSelectWidget):
    def get_data_icon(self, option_value):
        if option_value:
            # TODO; can this be optimised? PERFORMANCE
            return Category.objects.get(pk=int(option_value)).icon
        return option_value
