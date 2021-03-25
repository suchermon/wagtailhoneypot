from __future__ import absolute_import, unicode_literals

from django import forms
from wagtailcaptcha.forms import WagtailCaptchaFormBuilder
from wagtailhoney.widgets import HoneyPotFieldWidget


class HoneyPotFormField(forms.CharField):
    # Native Django Honeypot field
    def validate(self, value):
        # Make it validated no matter what
        return value


class WagtailHoneyPotFormBuilder(WagtailCaptchaFormBuilder):

    def create_honeypot_field(self, field, options):
        return HoneyPotFormField(widget=HoneyPotFieldWidget, **options)
