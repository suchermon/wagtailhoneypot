from django import forms

from wagtail.contrib.forms.forms import FormBuilder

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

from .widgets import HoneyPotFieldWidget


class WagtailCaptchaFormBuilder(FormBuilder):
    '''
    Original author: https://github.com/springload/wagtail-django-recaptcha/blob/master/wagtailcaptcha/forms.py

    Add support for ReCaptcha V3
    '''
    CAPTCHA_FIELD_NAME = 'wagtailcaptcha'

    @property
    def formfields(self):
        fields = super().formfields
        fields[self.CAPTCHA_FIELD_NAME] = ReCaptchaField(label='', widget=ReCaptchaV3)
        return fields

    class Meta:
        abstract = True


class HoneyPotFormField(forms.CharField):
    # Native Django Honeypot field
    def validate(self, value):
        # Make it validated no matter what
        return value


class WagtailHoneyPotFormBuilder(WagtailCaptchaFormBuilder):
    def create_honeypot_field(self, field, options):
        return HoneyPotFormField(widget=HoneyPotFieldWidget, **options)


def remove_captcha_field(form):
    form.fields.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)
    form.cleaned_data.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)
