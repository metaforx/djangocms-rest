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

djangocms-rest exposes django CMS content through a read-only REST API. It is based on the `Django REST framework <https://www.django-rest-framework.org/>`_ and provides OpenAPI 3 schema generation and a browsable API via `DRF Spectacular <https://github.com/tfranzel/drf-spectacular>`_.


Motivation
----------
Development has shifted more towards decoupled frontend apps due to easier scalability, the ability to serve multiple digital channels and work in specialized teams.
**djangocms-rest** provides a solution that serves both Django app content and Django CMS content via DRF, while preserving the intuitive Django CMS editing interface.

👉 **No need for yet another tech stack.**

Key Features
------------

* **Drop-in Ready** — Integrates seamlessly into existing or new django CMS projects.  
* **REST API** — DRF-based REST API exposing all django CMS content for SPAs, static sites, or mobile apps.  
* **Typed Endpoints** — Auto-generate OpenAPI schemas for pages, plugins, and custom serializers.  
* **Plugin Serialization** — Full support for all CMS plugins, easily extendable for custom ones.  
* **Multi-site Support** — Serve multiple websites from a single instance with isolated API responses.  
* **Multi-language Content** — Native integration with django CMS and django-parler translation systems.  
* **Preview & Draft Access** — Retrieve unpublished or draft content in your frontend for editor previews.  
* **Permissions & Authentication** — Built on Django and django CMS permission models for secure access control.  
* **Menus & Breadcrumbs** — Leverage django CMS’s built-in menu and navigation framework for structured output.  
* **Caching & Performance** — Optimized for Django’s cache backends, including Redis and Memcached.  

Quick Start
-----------

.. note::
    A running django CMS project is required. Follow the `Installing django CMS by hand <https://docs.django-cms.org/en/latest/introduction/01-install.html#installing-django-cms-by-hand>`_ guide to get started.


.. code-block:: bash

    # Install djangocms-rest
    pip install djangocms-rest


.. code-block:: python

    # Add to INSTALLED_APPS in your project's settings.py
    INSTALLED_APPS = [
        # ... other apps
        'djangocms_rest',
    ]

.. code-block:: python


    # Include URLs in your project's urls.py
    urlpatterns = [
        # ... other URLs
        path('api/', include('djangocms_rest.urls')),
    ]


.. code-block:: bash

    # Start the Django development server
    python manage.py runserver 8000

Test API
--------


`http://localhost:8080/api/languages/ <hhttp://localhost:8080/api/languages/>`_

.. code-block:: bash

   # Test the API endpoints and
    curl http://localhost:8000/api/languages



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
