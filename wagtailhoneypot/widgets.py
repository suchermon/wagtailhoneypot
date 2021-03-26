from django.forms.widgets import Input


class HoneyPotFieldWidget(Input):
    input_type = 'honeypot'
    template_name = 'wagtailhoneypot/forms/widgets/honeypot.html'

    class Media:
        css = {
            'all': ('hp_form.css',)
        }
        js = ('hp_form.js',)

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
