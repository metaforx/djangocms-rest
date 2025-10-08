Quick Start Guide
=================

This guide will help you get started with djangocms-rest quickly. We'll create a simple example that demonstrates the basic functionality.

Prerequisites
-------------

Make sure you have completed the :doc:`../tutorial/02-installation` guide before proceeding.

Basic Setup
-----------

1. **Create a new Django project** (if you don't have one):

.. code-block:: bash

    django-admin startproject myproject
    cd myproject

2. **Configure your settings**:

.. code-block:: python

    # settings.py
    import os
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = 'your-secret-key-here'

    DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
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
        
        # django CMS plugins
        'djangocms_link',
        'djangocms_text',
        
        # djangocms-rest
        'djangocms_rest',
        
        # Django REST Framework
        'rest_framework',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'cms.middleware.user.CurrentUserMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.language.LanguageCookieMiddleware',
    ]

    ROOT_URLCONF = 'myproject.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'sekizai.context_processors.sekizai',
                    'cms.context_processors.cms_settings',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'myproject.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True

    STATIC_URL = 'static/'
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # django CMS settings
    CMS_TEMPLATES = [
        ('page.html', 'Page'),
    ]

    # Django REST Framework settings
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 20,
    }

3. **Configure URLs**:

.. code-block:: python

    # urls.py
    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/cms/', include('djangocms_rest.urls')),
    ]

    if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

4. **Run migrations and create a superuser**:

.. code-block:: bash

    python manage.py migrate
    python manage.py createsuperuser

5. **Start the development server**:

.. code-block:: bash

    python manage.py runserver

Testing the API
---------------

Now let's test the API endpoints. **Important:** You must be logged into the Django CMS admin interface to access protected endpoints.

**Method 1: Using your browser (easiest)**

1. **Login to Django admin** at http://localhost:8000/admin/
2. **Visit the API endpoints** in the same browser session:
   * Pages list: http://localhost:8000/api/cms/pages/
   * Languages: http://localhost:8000/api/cms/languages/
   * Placeholders: http://localhost:8000/api/cms/placeholders/

**Method 2: Using curl with session cookies**

1. **Login and save cookies**:

.. code-block:: bash

    curl -c cookies.txt -X POST http://localhost:8000/admin/login/ \
         -d "username=admin&password=your-password&csrfmiddlewaretoken=your-csrf-token"

2. **Use cookies for API requests**:

.. code-block:: bash

    curl -b cookies.txt http://localhost:8000/api/cms/pages/
    curl -b cookies.txt http://localhost:8000/api/cms/languages/
    curl -b cookies.txt http://localhost:8000/api/cms/placeholders/

Creating Content via API
------------------------

Let's create a page using the API. **Remember:** You must be logged into Django admin first.

1. **Create a new page**:

.. code-block:: bash

    curl -X POST http://localhost:8000/api/cms/pages/ \
         -b cookies.txt \
         -H "Content-Type: application/json" \
         -d '{
           "title": "My First API Page",
           "slug": "my-first-api-page",
           "language": "en",
           "template": "page.html",
           "is_published": true
         }'

2. **Add content to a placeholder**:

.. code-block:: bash

    curl -X POST http://localhost:8000/api/cms/placeholders/1/plugins/ \
         -b cookies.txt \
         -H "Content-Type: application/json" \
         -d '{
           "plugin_type": "TextPlugin",
           "body": "This is content created via the API!"
         }'

Python Client Example
---------------------

Here's a Python example using the requests library with session authentication:

.. code-block:: python

    import requests

    # Base URL for your API
    base_url = 'http://localhost:8000/api/cms'

    # Create a session for authentication
    session = requests.Session()
    
    # Login to Django admin (you'll need to get the CSRF token first)
    login_data = {
        'username': 'admin',
        'password': 'your-password',
        'csrfmiddlewaretoken': 'your-csrf-token'  # Extract from login page
    }
    session.post('http://localhost:8000/admin/login/', data=login_data)

    # Get all pages using the authenticated session
    response = session.get(f'{base_url}/pages/')
    pages = response.json()
    print(f"Found {pages['count']} pages")

    # Get a specific page
    if pages['results']:
        page_id = pages['results'][0]['id']
        page_response = session.get(f'{base_url}/pages/{page_id}/')
        page = page_response.json()
        print(f"Page title: {page['title']}")

    # Get placeholders for a page
    if pages['results']:
        page_id = pages['results'][0]['id']
        placeholders_response = session.get(f'{base_url}/pages/{page_id}/placeholders/')
        placeholders = placeholders_response.json()
        print(f"Found {placeholders['count']} placeholders")

JavaScript Client Example
-------------------------

Here's a JavaScript example using fetch:

.. code-block:: javascript

    // Base URL for your API
    const baseUrl = 'http://localhost:8000/api/cms';

    // Function to get all pages
    async function getPages() {
        try {
            const response = await fetch(`${baseUrl}/pages/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    // Add your authentication headers here
                },
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('Pages:', data);
                return data;
            } else {
                console.error('Failed to fetch pages:', response.status);
            }
        } catch (error) {
            console.error('Error fetching pages:', error);
        }
    }

    // Function to create a new page
    async function createPage(pageData) {
        try {
            const response = await fetch(`${baseUrl}/pages/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Add your authentication headers here
                },
                body: JSON.stringify(pageData),
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('Created page:', data);
                return data;
            } else {
                console.error('Failed to create page:', response.status);
            }
        } catch (error) {
            console.error('Error creating page:', error);
        }
    }

    // Usage
    getPages();
    
    createPage({
        title: 'My JavaScript Page',
        slug: 'my-javascript-page',
        language: 'en',
        template: 'page.html',
        is_published: true
    });

Next Steps
----------

Now that you have a basic setup working, you can:

1. Explore the :doc:`../reference/index` to understand all available endpoints
2. Learn about :doc:`../how-to/02-authentication` and :doc:`../how-to/03-permissions`
3. Configure :doc:`../how-to/04-caching` for better performance
4. Check out the :doc:`../explanations/01-examples` for more advanced usage patterns

If you encounter any issues, check the :doc:`../tutorial/02-installation` troubleshooting section or visit the `GitHub repository <https://github.com/fsbraun/djangocms-rest>`_ for support. 