Installation
============

Requirements
------------

django CMS REST requires:

* Python 3.9 or higher
* Django 4.2 or higher
* django CMS 5.0 or higher
* Django REST Framework 3.14 or higher

Installation
-----------

Using pip
~~~~~~~~~

.. code-block:: bash

    pip install djangocms-rest

Using Poetry
~~~~~~~~~~~

.. code-block:: bash

    poetry add djangocms-rest

From source
~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/fsbraun/djangocms-rest.git
    cd djangocms-rest
    pip install -e .

Configuration
-------------

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
        
        # django CMS REST
        'djangocms_rest',
        
        # Django REST Framework
        'rest_framework',
    ]

2. Include the django CMS REST URLs in your main URL configuration:

.. code-block:: python

    from django.urls import path, include

    urlpatterns = [
        # ... other URL patterns
        path('api/cms/', include('djangocms_rest.urls')),
    ]

3. Configure Django REST Framework settings (optional but recommended):

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 20,
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
        ],
    }

**Note:** django CMS REST uses Session Authentication as the only authentication method. Users must be logged into the Django CMS admin interface to access protected API endpoints.

4. Run migrations:

.. code-block:: bash

    python manage.py migrate

5. Create a superuser (if you haven't already):

.. code-block:: bash

    python manage.py createsuperuser

Optional Dependencies
--------------------

For enhanced functionality, you can install additional packages:

.. code-block:: bash

    # For better performance
    pip install django-cacheops

    # For API documentation
    pip install drf-spectacular

    # For CORS support
    pip install django-cors-headers

Development Setup
----------------

For development, clone the repository and install in development mode:

.. code-block:: bash

    git clone https://github.com/fsbraun/djangocms-rest.git
    cd djangocms-rest
    
    # Install development dependencies
    pip install -e ".[dev]"
    
    # Run tests
    pytest
    
    # Build documentation
    cd docs
    make html

Verification
-----------

After installation, you can verify that django CMS REST is working correctly:

1. Start your Django development server:

.. code-block:: bash

    python manage.py runserver

2. **Login to Django admin** at http://localhost:8000/admin/

3. **Visit the API endpoints** in the same browser session:
   * Pages list: http://localhost:8000/api/cms/pages/
   * Languages: http://localhost:8000/api/cms/languages/
   * Placeholders: http://localhost:8000/api/cms/placeholders/

If you see JSON responses, the installation was successful! **Note:** You must be logged into the Django CMS admin interface to access these endpoints.

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

**ImportError: No module named 'djangocms_rest'**

Make sure you've added ``djangocms_rest`` to your ``INSTALLED_APPS`` and that the package is properly installed.

**404 errors on API endpoints**

Check that you've included the django CMS REST URLs in your main URL configuration.

**Permission denied errors**

Ensure that you're authenticated and have the necessary permissions to access the API endpoints.

**Django CMS not found**

Make sure django CMS is properly installed and configured in your Django project.

Getting Help
-----------

If you encounter any issues during installation:

* Check the `GitHub issues <https://github.com/fsbraun/djangocms-rest/issues>`_
* Review the `Django CMS documentation <https://docs.django-cms.org/>`_
* Consult the `Django REST Framework documentation <https://www.django-rest-framework.org/>`_ 