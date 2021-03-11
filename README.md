# Wagtail Honeypot

A simple implementation of Honeypot for catching spammers. When they fill in the `Honeypot` fields, their submission actually goes nowhere. Won't clog up our DB or anything. They will still see a "Thank you" is my way to tell them to go take a hike.

## Dependencies

I also like Captcha, so I built this on top of [wagtailcaptcha](https://github.com/springload/wagtail-django-recaptcha). You can still use the original wagtailcaptcha forms etc...

* Wagtail Django Captcha
* Django-captcha

## Installation

Get a [captcha key](https://www.google.com/recaptcha/intro/index.html)

### Install the apps

INSTALLED_APPS = [
    ...,
    'captcha',
    'wagtailcaptcha'
    'wagtailhoneypot',
    ...
]

### Environment Vars

```python
RECAPTCHA_PUBLIC_KEY = 'MyRecaptchaKey123'
RECAPTCHA_PRIVATE_KEY = 'MyRecaptchaPrivateKey456'
```

## Setup

```python
from wagtailcaptcha.models importWagtailCaptchaEmailForm
from wagtailhoneypot.models import WagtailHoneypotEmailForm


class FormField(AbstractFormField):
    CHOICES = FORM_FIELD_CHOICES + (('honeypot', 'HoneyPot Field'),)

    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')
    field_type = models.CharField(
        verbose_name=_('field type'),
        max_length=55,
        choices=CHOICES
    )


class FormPage(WagtailHoneypotEmailForm):
    ...
```

### Adding the Honey pots

When you create a page, you will now see a form field type named `HoneyPot Field`. I suggest set up: `Email`, `Name`, or `Phone` as `HoneyPot Field`, and the actual fields you want `Your Name`, `Your Email` or something less generic. Be creative!
