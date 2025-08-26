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

djangocms-rest provides comprehensive API endpoints for django CMS, enabling you to build headless CMS applications, mobile apps, or integrate django CMS content with other systems through RESTful APIs.

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

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 