# Wagtail Honeypot

A simple implementation of Honeypot for catching spammers. When they fill in the `Honeypot` fields, their submission actually goes nowhere. Won't clog up our DB or anything. They will still see the "Thank you" page is my way to tell them to go take a hike.

## Dependencies and thanks to other packages

* [Wagtail 2.12+](https://wagtail.io/)
* [ReCaptcha V2 & V3](https://www.google.com/recaptcha/admin/create)
* [Django-Recaptcha](https://github.com/praekelt/django-recaptcha)
* [FlashText](https://flashtext.readthedocs.io/)

## Installation

```bash
pip install -e 'git+https://github.com/suchermon/wagtailhoneypot.git@master#egg=wagtailhoneypot'

OR `pipenv`

pipenv install -e git+https://github.com/suchermon/wagtailhoneypot.git@master#egg=wagtailhoneypot
```

### Environment Vars

Get a set of [V2 OR V3 reCaptcha key](https://www.google.com/recaptcha/admin/create)

#### Basic Configs

```python
WAGTAIL_HONEYPOT_CAPTCHA_VERSION = 2

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

# For V3
RECAPTCHA_REQUIRED_SCORE = 0.6 # or lower, very janky if higher than .6

```

#### Additional `django-recaptcha` configs

[https://github.com/praekelt/django-recaptcha](https://github.com/praekelt/django-recaptcha)

### Install the apps

```python
INSTALLED_APPS = [
    ...,
    'captcha',
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
    <!-- Don't recommend `display: none`, too easy for spammer to catch that. See hp_form.css for example -->
    <div class="hp-formfield">
        {{ field }}
    </div>
  {% else %}
    <!-- render your other fields -->
  {% endif %}

  {% block scripts %}
    {{ form.media }}
  {% endblock %}
{% endfor %}
```


### Native Django form

```python

from wagtailhoneypot.forms import HoneyPotFormField
from wagtailhoneypot.widgets import HoneyPotFieldWidget

class ContactForm(forms.Form):
    phonenumber = HoneyPotField(widget=HoneyPotFieldWidget())

```

If you use the above, the JS is required to remove the `required` attribute from the `data-js="hp-formfield"` or you can write your own in jquery or whatever to remove them on submit. I included a vanilla JS to do so. So make sure you include the scripts.


```
{% block scripts %}
    {{ form.media }}
{% endblock %}
```

## Adding the Honey pots

When you create a wagtail `formpage`, you will now see a form field type named `HoneyPot Field` at the very bottom. I suggest set up: `Email`, `Name`, or `Phone` as `HoneyPot Field`, and the actual fields you want `Your Name`, `Your Email` or something less generic. Be creative!

## Additional Settings

They still got through our honey pots?!! Well, you can go to **Settings -> Wagtailhoneypot**, you can add:

* `domains` - add as many as domains you want, it'll look through the `EmailInput` fields and filter those out.
* `keywords` - it'll look through the `Textarea` input fields and look for those keywords within and filter them out.
