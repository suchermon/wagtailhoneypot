import os
from setuptools import find_packages, setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


long_desc = open('README.md', 'rb').read().decode('utf-8')


def get_requirements_tests():
    with open('requirements.txt') as f:
        return f.readlines()


setup(
    name='wagtailhoneypot',
    version='1.0.2',
    description='A wagtail package built on top of Django-captcha to add some honeypot fields for wagtail form builder, honeypot widgets can also be used with native Django forms.',
    long_desciption=long_desc,
    author='Mon Sucher',
    author_email='supawaza@gmail.com',
    url='https://github.com/suchermon/wagtailhoneypot.git',
    include_package_data=True,
    install_requires=[
        'flashtext',
        'django>3,<4',
        'django-recaptcha',
        'wagtail>=2.12',
    ],
    license='MIT',
    keywords=['django', 'reCAPTCHA', 'honeypot', 'forms', 'anti-spam', 'reCAPCHA v2'],
    packages=find_packages(),
    package_data={'wagtailhoneypot': [
        "templates/wagtailhoneypot/*.html",
        "templates/wagtailhoneypot/*/*.html",
    ]},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0.3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
