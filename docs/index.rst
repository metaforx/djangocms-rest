djangocms-rest
============================

.. image:: https://img.shields.io/badge/python-3.9+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python version

.. image:: https://img.shields.io/badge/django-4.2+-green.svg
   :target: https://www.djangoproject.com/
   :alt: Django version

.. image:: https://img.shields.io/badge/django--cms-5.0+-orange.svg
   :target: https://www.django-cms.org/
   :alt: django CMS version

.. image:: https://img.shields.io/badge/license-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause
   :alt: License

*Headless content delivery with django CMS for modern, typed frontend apps.*

djangocms-rest lets you use `django CMS <https://www.django-cms.org/>`_ as a headless backend for modern, typed frontend applications, while preserving the intuitive django CMS editing interface. This makes it possible to build Django apps that combine CMS-driven content with decoupled frontend frameworks.

It can be added at any stage of a project and also runs alongside a traditional django CMS setup. This allows you to serve content not only to websites but also to mobile apps, digital signage, or any other frontend channel.

djangocms-rest exposes django CMS content through a read-only REST API. It is based on the `Django REST framework <https://www.django-rest-framework.org/>`_ and provides OpenAPI 3 schema generation and a browsable API via `DRF Spectacular <https://github.com/tfranzel/drf-spectacular>`_.





Key Features
------------

* **Complete Page API**: Full CRUD operations for django CMS pages
* **Placeholder Management**: Access and manage page placeholders and their content
* **Plugin Support**: Serialize and manage CMS plugins including text, links, and custom plugins
* **Multi-language Support**: Handle multiple languages and translations
* **Caching**: Built-in caching for improved performance
* **Authentication**: Session-based authentication integrated with Django CMS admin
* **Permissions**: Fine-grained permission control using Django's permission system

Quick Start
-----------

.. code-block:: python

    # Install djangocms-rest
    pip install djangocms-rest

    # Add to INSTALLED_APPS
    INSTALLED_APPS = [
        # ... other apps
        'djangocms_rest',
    ]

    # Include URLs
    urlpatterns = [
        # ... other URLs
        path('api/cms/', include('djangocms_rest.urls')),
    ]

.. toctree::
   :maxdepth: 2

   tutorial/index
   how-to/index
   explanations/index
   reference/index
   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
