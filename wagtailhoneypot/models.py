from django.forms import Textarea
from django.db import models
from django.utils.translation import ugettext_lazy as _

from flashtext import KeywordProcessor

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractForm
from wagtail.contrib.settings.models import BaseSetting, register_setting

from .forms import WagtailCaptchaFormBuilder, WagtailHoneyPotFormBuilder, remove_captcha_field


@register_setting
class WagtailHoneyPotSettings(BaseSetting):
    domains = models.TextField(
        blank=True,
        verbose_name=_('Blocked by domains'),
        help_text=_('Ex: spammers.com, one per line please')
    )
    keywords = models.TextField(
        blank=True,
        verbose_name=_('Keywords'),
        help_text=_('Separate each keyword with comma or new line')
    )

    panels = [
        FieldPanel('domains', widget=Textarea(attrs={'placeholder': _('One domain per line')})),
        FieldPanel('keywords', widget=Textarea(attrs={'placeholder': _('Separate by commas')}))
    ]


class WagtailCaptchaEmailForm(AbstractEmailForm):
    """Pages implementing a captcha form with email notification should inhert from this"""

    form_builder = WagtailCaptchaFormBuilder

    def process_form_submission(self, form):
        remove_captcha_field(form)
        return super(WagtailCaptchaEmailForm, self).process_form_submission(form)

    class Meta:
        abstract = True


class WagtailCaptchaForm(AbstractForm):
    """Pages implementing a captcha form should inhert from this"""

    form_builder = WagtailCaptchaFormBuilder

    def process_form_submission(self, form):
        remove_captcha_field(form)
        return super(WagtailCaptchaForm, self).process_form_submission(form)

    class Meta:
        abstract = True


class WagtailHoneypotForm(WagtailCaptchaForm):
    """Pages implementing a honeypot form should inherit from this"""
    form_builder = WagtailHoneyPotFormBuilder

    def __init__(self, *args, **kwargs):
        self.kw_processor = KeywordProcessor()
        self.HONEYPOT_FIELDS = []
        super().__init__(*args, **kwargs)

    def get_settings(self, request):
        try:
            self.settings = WagtailHoneyPotSettings.for_request(request)
        except WagtailHoneyPotSettings.DoesNotExist:
            self.settings = None

        return self.settings

    def process_form_submission(self, form):

        if hasattr(self, 'settings'):
            honeypot_settings = self.settings

        for field in form:
            widget_type = field.field.widget.__class__.__name__

            if not widget_type.startswith('Recaptcha'):
                field_value = form.cleaned_data[field.name]

                if widget_type == 'HoneyPotFieldWidget':
                    if field_value:
                        return None
                    else:
                        self.HONEYPOT_FIELDS.append(field.name)

                if honeypot_settings and widget_type == 'EmailInput':
                    domain = field_value.split('@')[-1]
                    if domain in [x for x in honeypot_settings.domains.split('\r\n')]:
                        return None

                if honeypot_settings and widget_type == 'Textarea':
                    keywords = [x.strip() for x in honeypot_settings.keywords.split(',')]
                    self.kw_processor.add_keywords_from_list(keywords)

                    if self.kw_processor.extract_keywords(field_value):
                        return None

        for field in self.HONEYPOT_FIELDS:
            form.cleaned_data.pop(field)
            form.fields.pop(field)

        return super().process_form_submission(form)

    def get_data_fields(self):
        data_fields = [
            (field.clean_name, field.label)
            for field in self.get_form_fields() if field.field_type != 'honeypot'
        ]
        return data_fields

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.get_settings(request)
        return super().serve(request, *args, **kwargs)

    class Meta:
        abstract = True


class WagtailHoneypotEmailForm(WagtailHoneypotForm, WagtailCaptchaEmailForm):
    """Pages implementing a honeypot form with email notification should inherit from this"""
    form_builder = WagtailHoneyPotFormBuilder

    class Meta:
        abstract = True
