djangocms-rest
============================

.. image:: https://img.shields.io/badge/python-3.9+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python version

.. image:: https://img.shields.io/badge/Django-4.2+-green.svg
   :target: https://www.Djangoproject.com/
   :alt: Django version

.. image:: https://img.shields.io/badge/Django--cms-5.0+-orange.svg
   :target: https://www.Django-cms.org/
   :alt: Django CMS version

.. image:: https://img.shields.io/badge/license-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause
   :alt: License

*Headless content delivery with Django CMS for modern, typed frontend apps.*

djangocms-rest lets you use `Django CMS <https://www.Django-cms.org/>`_ as a headless backend for modern, typed frontend applications, while preserving the intuitive Django CMS editing interface. This makes it possible to build Django apps that combine CMS-driven content with decoupled frontend frameworks.

djangocms-rest exposes Django CMS content through a read-only REST API. It is based on the `Django REST framework <https://www.Django-rest-framework.org/>`_ and provides OpenAPI 3 schema generation and a browsable API via `DRF Spectacular <https://github.com/tfranzel/drf-spectacular>`_.


Motivation
----------
Web development is increasingly adopting decoupled front ends for greater scalability, multi-channel content and team flexibility.
**djangocms-rest** provides a solution to use Django CMS also as a headless backend. 


👉 **You already use Django CMS? No need for yet another tech stack.**

Key Features
------------

* **Easy integration** — Integrates effortlessly into existing Django CMS projects.  
* **REST API** — DRF-based API exposing Django CMS content for SPAs, static sites, and mobile apps.  
* **Typed Endpoints** — Auto-generate OpenAPI schemas for pages, plugins, and custom serializers.  
* **Plugin Serialization** — Basic support for all CMS plugins, easily extendable for custom output.  
* **Multi-site Support** — Serve multiple websites from a single instance with isolated API responses.  
* **Multi-language Content** — Use the robust i18n integartion of Django CMS in your frontend.   
* **Preview & Draft Access** — Fetch unpublished or draft content in your frontend for editor previews.  
* **Permissions & Authentication** — Uses DRF- and Django-permissions for secure access control.  
* **Menus & Breadcrumbs** — Exposes the built-in navigation handlers from Django CMS.  
* **Caching & Performance** — Works with Django cache backends like Redis and Memcached.  


Quick Start
-----------

.. note::
    A running Django CMS project is required. Follow the `Installing Django CMS by hand <https://docs.Django-cms.org/en/latest/introduction/01-install.html#installing-Django-cms-by-hand>`_ guide to get started.


.. code-block:: bash

    # Install djangocms-rest
    pip install djangocms-rest


.. code-block:: python

    # Add to INSTALLED_APPS in your project's settings.py
    INSTALLED_APPS = [
        # ... other apps
        'Djangocms_rest',
    ]

.. code-block:: python


    # Include URLs in your project's urls.py
    urlpatterns = [
        # ... other URLs
        path('api/', include('Djangocms_rest.urls')),
    ]


.. code-block:: bash

    # Start the Django development server
    python manage.py runserver 8000

Test API
--------


`http://localhost:8080/api/languages/ <hhttp://localhost:8080/api/languages/>`_

.. code-block:: bash

   # Test the API endpoints
    curl http://localhost:8000/api/languages

If you see a response like this, you're good to go:

.. code-block:: json

    [
      {
        "code": "en",
        "name": "English",
        "public": true,
        "fallbacks": [
          "en"
        ],
        "redirect_on_fallback": true,
        "hide_untranslated": false
      },
      {
        "code": "de",
        "name": "Deutsch",
        "public": false,
        "fallbacks": [
          "en"
        ],
        "redirect_on_fallback": true,
        "hide_untranslated": true
      }
    ]

.. toctree::
   :maxdepth: 1
   :hidden:

   tutorial/index
   how-to/index
   explanations/index
   reference/index
   contributing
   changelog

