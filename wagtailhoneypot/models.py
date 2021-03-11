from django.forms import Textarea
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from flashtext import KeywordProcessor

from wagtail.admin.edit_handlers import FieldPanel
from wagtailcaptcha.models import WagtailCaptchaForm, WagtailCaptchaEmailForm
from wagtail.contrib.settings.models import BaseSetting, register_setting

from .forms import WagtailHoneyPotFormBuilder


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


class WagtailHoneypotForm(WagtailCaptchaForm):
    """Pages implementing a honeypot form should inherit from this"""
    form_builder = WagtailHoneyPotFormBuilder

    def __init__(self, *args, **kwargs):
        self.kw_processor = KeywordProcessor()
        super().__init__(*args, **kwargs)

    def get_settings(self, request):
        try:
            self.settings = WagtailHoneyPotSettings.for_site(settings.SITE_ID)
        except WagtailHoneyPotSettings.DoesNotExist:
            self.settings = None

        return self.settings

    def process_form_submission(self, form):
        HONEYPOT_FIELDS = []

        if hasattr(self, 'settings'):
            honeypot_settings = self.settings

        for field in form:
            widget_type = field.field.widget.__class__.__name__

            print(widget_type)

            if not widget_type.startswith('Recaptcha'):
                field_value = form.cleaned_data[field.name]

                if widget_type == 'HoneyPotFieldWidget':
                    if field_value:
                        return None
                    else:
                        HONEYPOT_FIELDS.append(field.name)

                if honeypot_settings and widget_type == 'EmailInput':
                    domain = field_value.split('@')[-1]
                    if domain in [x for x in honeypot_settings.domains.split('\r\n')]:
                        print('Spam email address')
                        return None

                if honeypot_settings and widget_type == 'Textarea':
                    keywords = [x.strip() for x in honeypot_settings.keywords.split(',')]
                    self.kw_processor.add_keywords_from_list(keywords)

                    if self.kw_processor.extract_keywords(field_value):
                        return None

        for field in HONEYPOT_FIELDS:
            form.cleaned_data.pop(field)
            form.fields.pop(field)

        return super().process_form_submission(form)

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
