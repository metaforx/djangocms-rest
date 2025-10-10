Installation
============

Requirements
------------

djangocms-rest requires:

* Python 3.9 or higher
* Django 4.2 or higher
* django CMS 4.2 or higher (5.0 preferred)
* Django REST Framework 3.14 or higher

Installation
------------
.. note::
    A running Django CMS project is required. Follow the `Installing Django CMS by hand <https://docs.django-cms.org/en/latest/introduction/01-install.html#installing-django-cms-by-hand>`_ guide to get started.

Using Poetry
~~~~~~~~~~~~

We recommend using ``Poetry`` to manage your dependencies. It it is used as default for this documentation.
``pip`` can be used as equivalent.

.. code-block:: bash

    poetry add djangocms-rest

Using pip
~~~~~~~~~

.. code-block:: bash

    pip install djangocms-rest


Latest from source
~~~~~~~~~~~~~~~~~~~~~~~~
For the latest features, you can install the a version from the GitHub repository at your own risk:

.. code-block:: bash

    poetry add git+https://github.com/fsbraun/djangocms-rest.git

.. code-block:: bash

    # install a specific branch
    poetry add git+https://github.com/fsbraun/djangocms-rest.git@feat/extended-search 

Basic Configuration
--------------------

1. Add ``djangocms_rest`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # ... other Django apps
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        
        # django CMS
        'cms',
        'menus',
        'treebeard',
        'sekizai',
        
        # django CMS plugins (optional but recommended)
        'djangocms_link',
        'djangocms_text',
        
        # djangocms-rest
        'djangocms_rest',
    ]

2. Include the djangocms-rest URLs in your project's main URL configuration:

.. code-block:: python
    
    # demo_cms/urls.py
    from django.urls import path, include

    urlpatterns = [
        # ... other URL patterns
        path('api/', include('djangocms_rest.urls')), #api can be changed to your liking
    ]

2.1 Add optional API prefix

Alternatively, you can put the API under a specific path, like ``api/cms/``. 
This is handy if you want to have a separate API for different parts of your app.

.. code-block:: python

    from django.urls import path, include

    urlpatterns = [
        # ... other URL patterns
        path('api/', include('my_django_rest_app.urls')),
        path('api/cms/', include('djangocms_rest.urls')), 
    ]

.. note::
    When you autocreate clients and types from OpenAPI specification with tools like `heyapi.dev <https://heyapi.dev/>`_, this will also affect the naming of those components and types,eg.
    ``RetrieveLanguages`` will become ``CmsRetrieveLanguages`` in the client sdk.

CORS Support
------------

If you want to serve the API from a different domain, you can use the ``CorsMiddleware`` to enable CORS.
This is optional, but likely needed for security reasons with decoupled frontend apps.

Docs
~~~~
- `Django CORS Headers <https://github.com/adamchainz/django-cors-headers>`_


Configuration
~~~~~~~~~~~~~

.. code-block:: bash

    poetry add django-cors-headers


.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
    ...,
    "corsheaders",
    ...,
    ]

    CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    ]


.. code-block:: python

    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
    ]


Languages Support
-----------------

- djnagocms-rest supports languages out of the box. 
- Djnago CMS needs dob be configured to use languages. 
- A single language must always be set in order to use the API.

Docs
~~~~
- `Django CMS - Internationalisation and Localisation <https://docs.django-cms.org/en/stable/explanation/i18n.html>`_
- `Django CMS - Language configuration <https://docs.django-cms.org/en/stable/reference/configuration.html#internationalisation-and-localisation-i18n-and-l10n>`_
- `Django CMS - Howto - Languages <https://docs.django-cms.org/en/latest/how_to/02-languages.html>`_

Configuration
~~~~~~~~~~~~~

This is a simple configuration to get you started. Follow the Django CMS documentation to configure languages in-depth.

.. code-block:: python

    # settings.py

    # Language settings
    LANGUAGE_CODE = "en"

    USE_I18N = True

    LANGUAGES = (
        ("de", _("German")),
        ("en", _("English")),
    )

    CMS_LANGUAGES = {
        1: [
            {
                "code": "en",
                "name": "English",
                "public": True,
            },
            {
                "code": "de",
                "name": _("Deutsch"),
                "public": False,
                "hide_untranslated": True,
            },
        ],
        "default": {
            "fallbacks": ["en"],
            "redirect_on_fallback": True,
            "public": True,
            "hide_untranslated": False,
        },
    }

    MIDDLEWARE = [
        ...,
        "cms.middleware.language.LanguageCookieMiddleware",
        ...,
    ]


.. code-block:: python
    
    # urls.py
    # example configuration
    urlpatterns += i18n_patterns(
        path('admin/', include(admin.site.urls)),
        path('', include('cms.urls')),
        prefix_default_language=False,
    )


Multi-Site Support
------------------

djangocms-rest supports 2 ways to handle multi-site support:

1. **Multi-Instance Setup:** Follow the guide howto setup a multi-site django CMS project. 
2. **Single Instance Setup:** Using the ``SiteContextMiddleware`` to set the site context on the request.

**Option 1:**

1. foo.example.com/api/cms/pages/ < REQUEST > Content foo site  
2. bar.example.com/api/cms/pages/ < REQUEST > Content bar site

**Option 2:**

1. cms.example.com/api/cms/pages/ < REQUEST HEADERS X-Site-ID: 1 > Content foo site
2. cms.example.com/api/cms/pages/ < REQUEST HEADERS X-Site-ID: 2 > Content bar site

If you want to serve multiple sites from a single instance, you can use the ``SiteContextMiddleware`` to set the site context on the request.
This requires django `sites` framework to be installed and configured.

Your can pass the site ID in the request headers with the ``X-Site-ID`` property set to the site ID. 
The Middleware will then set the site context on the request.

Docs
~~~~
- `Django Sites <https://docs.djangoproject.com/en/5.2/ref/contrib/sites/>`_
- `Enabling Sites Framework <https://docs.djangoproject.com/en/5.2/ref/contrib/sites/#enabling-the-sites-framework>`_
- `Django CMS - Multi-Site installation <https://docs.django-cms.org/en/stable/how_to/03-multi-site.html#multi-site-installation>`_

For Option 2, you do not need to configure the webserver running the CMS as the frontend runs headless on a different domain.
Otherwise follow the guide how to setup a multi-site django CMS project.


Configuration
~~~~~~~~~~~~~

.. code-block:: python
    
    INSTALLED_APPS = [
        ...
        'django.contrib.sites',
        ...
    ]

    SITE_ID = 1

**Manage Sites in Django Admin**

- Go to Django Admin → Sites
- Add/edit sites with domain and name

Example:

.. code-block:: json

    [
      {
        "id": 1,
        "domain": "foo.example.com",
        "name": "Foo Site"
      },
      {
        "id": 2,
        "domain": "bar.example.com", 
        "name": "Bar Site"
      }
    ]

.. code-block:: python

    MIDDLEWARE = [
        # Required for cross-origin requests (frontend on different domain)
        "corsheaders.middleware.CorsMiddleware",

        #before other middleware that depends on the site context
        "djangocms_rest.middleware.SiteContextMiddleware", 

        # other django and django CMS middleware (depends on your setup)
        ...
    ]

Testing
~~~~~~~

1. Create a test home page for each site in the Django admin.
2. Publish the pages.
3. Test the API endpoints with the ``X-Site-ID`` header set to the site ID.


.. code-block:: bash

    # pages endpoint without path will return the home page for the site
    curl -H "X-Site-ID: 2" http://localhost:8000/api/cms/pages/

.. note::
    The ``X-Site-ID`` header is not required. If not set, the middleware will use the current site defined in the settings.

Implementation Guide
~~~~~~~~~~~~~~~~~~~~

If the basic configuration is working you can embed it into your frontend app.

- :doc:`../how-to/01-use-multi-site`

OpenAPI Specification
---------------------

djangocms-rest is fully typed and supports OpenAPI 3 schema generation using `drf-spectacular <https://drf-spectacular.readthedocs.io/en/latest/>`_.
Swagger UI and Redoc are also supported and highly recommended for development.

Docs
~~~~

Follow the drf-spectacular documentation to configure the schema generation in-depth.

- `drf-spectacular <https://drf-spectacular.readthedocs.io/en/latest/>`_

Configuration
~~~~~~~~~~~~~

This is a simple configuration to get you started.

.. code-block:: bash

    poetry add drf-spectacular


.. code-block:: python

    INSTALLED_APPS = [
        ...
        'drf_spectacular',
        ...
    ]

    # Add REST Framework settings
    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        ... # other settings
    }


    # recommended settings, but not required
    SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # other settings
    }

.. code-block:: python
    urlpatterns = [
        ...
        # OpenAPI schema and documentation
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path("api/schema-json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ...
    ]
..

 
.. note::

    Using `heyapi.dev <https://heyapi.dev/>`_ you can generate a client sdk for your frontend app.


Testing
~~~~~~~

 You can check now your:

 - API documentation at `http://localhost:8000/api/docs/ <http://localhost:8000/api/docs/>`_
 - OpenAPI specification as JSON at `http://localhost:8000/api/schema-json/ <http://localhost:8000/api/schema-json/>`_


Implementation Guide
~~~~~~~~~~~~~~~~~~~~

- :doc:`../how-to/05-sdk-generation`