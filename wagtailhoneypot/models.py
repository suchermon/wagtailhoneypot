from wagtailcaptcha.models import WagtailCaptchaForm, WagtailCaptchaEmailForm

from .forms import WagtailHoneyPotFormBuilder


class WagtailHoneypotForm(WagtailCaptchaForm):
    """Pages implementing a honeypot form should inherit from this"""
    form_builder = WagtailHoneyPotFormBuilder

    def process_form_submission(self, form):
        HONEYPOT_FIELDS = []
        for field in form:
            if hasattr(field.field.widget, 'input_type'):
                if field.field.widget.input_type == 'honeypot':
                    if form.cleaned_data[field.name]:
                        return None
                    else:
                        HONEYPOT_FIELDS.append(field.name)

        for field in HONEYPOT_FIELDS:
            form.cleaned_data.pop(field)
            form.fields.pop(field)

        return super().process_form_submission(form)

    class Meta:
        abstract = True


class WagtailHoneypotEmailForm(WagtailHoneypotForm, WagtailCaptchaEmailForm):
    """Pages implementing a honeypot form with email notification should inherit from this"""
    form_builder = WagtailHoneyPotFormBuilder

    class Meta:
        abstract = True
