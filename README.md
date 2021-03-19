# Wagtail Honeypot

A simple implementation of Honeypot for catching spammers. When they fill in the `Honeypot` fields, their submission actually goes nowhere. Won't clog up our DB or anything. They will still see a "Thank you" is my way to tell them to go take a hike.

## Dependencies and thanks to other packages

I also like Captcha, so I built this on top of [Wagtail Recaptcha](https://github.com/springload/wagtail-django-recaptcha). You can still use the original `wagtailcaptcha` forms etc...

* Wagtail 2.12+
* [Wagtail Django Recaptcha](https://github.com/springload/wagtail-django-recaptcha)
* [Django-Recaptcha](https://github.com/praekelt/django-recaptcha)
* [FlashText](https://flashtext.readthedocs.io/)

## Installation

```bash
`pip install -e 'git+https://github.com/suchermon/wagtailhoneypot.git@master#egg=wagtailhoneypot'`

OR `pipenv`

`pipenv install -e git+https://github.com/suchermon/wagtailhoneypot.git@master#egg=wagtailhoneypot`
```

### Environment Vars

Get a [captcha key](https://www.google.com/recaptcha/admin/create)

```python
RECAPTCHA_PUBLIC_KEY = 'MyRecaptchaKey123'
RECAPTCHA_PRIVATE_KEY = 'MyRecaptchaPrivateKey456'
```

### Install the apps

```python
INSTALLED_APPS = [
    ...,
    'captcha',
    'wagtailcaptcha'
    'wagtailhoneypot',
    ...
]
```

Run `./manage.py migrate`

## Setup

```python

# form_page.py

from wagtail.contrib.forms.models import AbstractFormField, FORM_FIELD_CHOICES
from wagtailhoneypot.models import WagtailHoneypotForm, WagtailHoneypotEmailForm


class FormField(AbstractFormField):
    CHOICES = FORM_FIELD_CHOICES + (('honeypot', 'HoneyPot Field'),)

    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')
    field_type = models.CharField(
        verbose_name=_('field type'),
        max_length=55,
        choices=CHOICES
    )

# Just a formpage
class FormPage(WagtailHoneypotForm):
    ...


# For Email Form
class FormPage(WagtailHoneypotEmailForm):
    ...
```


```html

<!-- form_page.html -->

{% for field in form %}
  {% if field.field.widget.input_type == 'honeypot' %}
    <div style="visibility: hidden; height: 0;">
        {{ field }}
    </div>
  {% else %}
    <!-- render your other fields -->
  {% endif %}
{% endfor %}
```

## Adding the Honey pots

When you create a wagtail `formpage`, you will now see a form field type named `HoneyPot Field` at the very bottom. I suggest set up: `Email`, `Name`, or `Phone` as `HoneyPot Field`, and the actual fields you want `Your Name`, `Your Email` or something less generic. Be creative!

## Additional Settings

They still got through our honey pots?!! Well, you can go to **Settings -> Wagtailhoneypot**, you can add:

* `domains` - add as many as domains you want, it'll look through the `EmailInput` fields and filter those out.
* `keywords` - it'll look through the `Textarea` input fields and look for those keywords within and filter them out.
