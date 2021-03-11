from __future__ import absolute_import, unicode_literals

from django import forms

from wagtailcaptcha.forms import WagtailCaptchaFormBuilder


class HoneyPotFieldWidget(forms.widgets.Input):
    input_type = 'honeypot'
    template_name = 'wagtailhoneypot/forms/widgets/honeypot.html'

    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}

        default_options = {
            'autocomplete': 'off',
        }

        options = kwargs.get('options', {})
        default_options.update(options)
        for key, val in default_options.items():
            attrs[key] = val

        super().__init__(attrs)


class WagtailHoneyPotFormBuilder(WagtailCaptchaFormBuilder):

    def create_honeypot_field(self, field, options):
        return forms.CharField(widget=HoneyPotFieldWidget, **options)
