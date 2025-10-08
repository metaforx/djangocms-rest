Configuration
=============

djangocms-rest provides various configuration options to customize its behavior. This guide covers all available settings.

Django REST Framework Settings
------------------------------

Configure Django REST Framework settings in your Django settings file:

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 20,
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
        ],
        'DEFAULT_PARSER_CLASSES': [
            'rest_framework.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser',
        ],
        'DEFAULT_FILTER_BACKENDS': [
            'rest_framework.filters.SearchFilter',
            'rest_framework.filters.OrderingFilter',
        ],
        'DEFAULT_THROTTLE_CLASSES': [
            'rest_framework.throttling.AnonRateThrottle',
            'rest_framework.throttling.UserRateThrottle',
        ],
        'DEFAULT_THROTTLE_RATES': {
            'anon': '100/hour',
            'user': '1000/hour',
        ],
    }

djangocms-rest Settings
-----------------------

Add these settings to your Django settings file to customize djangocms-rest behavior:

.. code-block:: python

    # djangocms-rest specific settings
    DJANGOCMS_REST = {
        # Cache settings
        'CACHE_ENABLED': True,
        'CACHE_TIMEOUT': 300,  # 5 minutes
        'CACHE_KEY_PREFIX': 'djangocms_rest',
        
        # Serialization settings
        'INCLUDE_PLACEHOLDERS': True,
        'INCLUDE_PLUGINS': True,
        'MAX_DEPTH': 3,
        
        # Permission settings
        'DEFAULT_PERMISSIONS': [
            'cms.add_page',
            'cms.change_page',
            'cms.delete_page',
            'cms.view_page',
        ],
        
        # Language settings
        'DEFAULT_LANGUAGE': 'en',
        'SUPPORTED_LANGUAGES': ['en', 'de', 'fr'],
        
        # Pagination settings
        'PAGE_SIZE': 20,
        'MAX_PAGE_SIZE': 100,
        
        # API settings
        'API_VERSION': '1.0',
        'ENABLE_DOCS': True,
        
        # Security settings
        'ALLOW_ANONYMOUS_READ': False,
        'REQUIRE_AUTHENTICATION': True,
        
        # Performance settings
        'USE_SELECT_RELATED': True,
        'USE_PREFETCH_RELATED': True,
        'OPTIMIZE_QUERIES': True,
    }

Setting Reference
-----------------

.. list-table:: DJANGOCMS_REST Settings
   :header-rows: 1
   :widths: 20 20 20 40

   * - Setting
     - Type
     - Default
     - Description
   * - CACHE_ENABLED
     - boolean
     - True
     - Enable/disable caching for API responses
   * - CACHE_TIMEOUT
     - integer
     - 300
     - Cache timeout in seconds
   * - CACHE_KEY_PREFIX
     - string
     - 'djangocms_rest'
     - Prefix for cache keys
   * - INCLUDE_PLACEHOLDERS
     - boolean
     - True
     - Include placeholder data in page responses
   * - INCLUDE_PLUGINS
     - boolean
     - True
     - Include plugin data in placeholder responses
   * - MAX_DEPTH
     - integer
     - 3
     - Maximum depth for nested content
   * - DEFAULT_PERMISSIONS
     - list
     - ['cms.add_page', ...]
     - Default permissions required for API access
   * - DEFAULT_LANGUAGE
     - string
     - 'en'
     - Default language for content
   * - SUPPORTED_LANGUAGES
     - list
     - ['en', 'de', 'fr']
     - List of supported language codes
   * - PAGE_SIZE
     - integer
     - 20
     - Default page size for pagination
   * - MAX_PAGE_SIZE
     - integer
     - 100
     - Maximum page size for pagination
   * - API_VERSION
     - string
     - '1.0'
     - API version string
   * - ENABLE_DOCS
     - boolean
     - True
     - Enable API documentation endpoints
   * - ALLOW_ANONYMOUS_READ
     - boolean
     - False
     - Allow anonymous users to read content
   * - REQUIRE_AUTHENTICATION
     - boolean
     - True
     - Require authentication for all endpoints
   * - USE_SELECT_RELATED
     - boolean
     - True
     - Use select_related for optimized queries
   * - USE_PREFETCH_RELATED
     - boolean
     - True
     - Use prefetch_related for optimized queries
   * - OPTIMIZE_QUERIES
     - boolean
     - True
     - Enable query optimization

Cache Configuration
-------------------

djangocms-rest supports various cache backends. Configure caching in your Django settings:

.. code-block:: python

    # Redis cache backend (recommended for production)
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

    # Or use database cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'djangocms_rest_cache',
        }
    }

    # Or use file system cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
        }
    }

Authentication Configuration
----------------------------

djangocms-rest uses Session Authentication as the only authentication method. Configure it in your Django settings:

.. code-block:: python

    # Session authentication (default and only supported method)
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    }

**Note:** Users must be logged into the Django CMS admin interface to access protected API endpoints. The API uses the same session-based authentication as the admin interface.

Permission Configuration
------------------------

Customize permissions for different user groups:

.. code-block:: python

    # Custom permission classes
    from rest_framework.permissions import IsAuthenticated, IsAdminUser
    from djangocms_rest.permissions import CMSPagePermission

    class CustomPagePermission(CMSPagePermission):
        def has_permission(self, request, view):
            # Custom permission logic
            if request.user.is_superuser:
                return True
            return super().has_permission(request, view)

    # Apply custom permissions to views
    from djangocms_rest.views import PageViewSet

    class CustomPageViewSet(PageViewSet):
        permission_classes = [CustomPagePermission] 