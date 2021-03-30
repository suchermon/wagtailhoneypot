from django import forms
from wagtail.contrib.forms.forms import FormBuilder
from .widgets import HoneyPotFieldWidget

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class HoneyPotFormField(forms.CharField):
    # Native Django Honeypot field
    def validate(self, value):
        # Make it validated no matter what
        return value


class WagtailCaptchaFormBuilder(FormBuilder):
    CAPTCHA_FIELD_NAME = 'wagtailcaptcha'

    ''' Extend from https://github.com/springload/wagtail-django-recaptcha/blob/master/wagtailcaptcha/forms.py to support Recaptch V3 - Project is dead'''

    @property
    def formfields(self):
        # Add wagtailcaptcha to formfields property
        fields = super(WagtailCaptchaFormBuilder, self).formfields
        fields[self.CAPTCHA_FIELD_NAME] = ReCaptchaField(label='', widget=ReCaptchaV3)

        return fields


class WagtailHoneyPotFormBuilder(WagtailCaptchaFormBuilder):

    def create_honeypot_field(self, field, options):
        return HoneyPotFormField(widget=HoneyPotFieldWidget, **options)


def remove_captcha_field(form):
    form.fields.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)
    form.cleaned_data.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)
