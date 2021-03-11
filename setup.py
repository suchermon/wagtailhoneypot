import os
from setuptools import find_packages, setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


with open('README.md') as readme:
    README = readme.read()


def get_requirements_tests():
    with open('requirements.txt') as f:
        return f.readlines()


setup(
    name='wagtailhoneypot',
    include_package_data=True,
    install_requires=[
        'flashtext',
        'django-recaptcha',
        'wagtail-django-recaptcha',
        'wagtail>=2.12',
    ],
    packages=find_packages('.'),
    package_data={'wagtailhoneypot': [
        "templates/wagtailhoneypot/*.html",
        "templates/wagtailhoneypot/*/*.html",
    ]},
)
