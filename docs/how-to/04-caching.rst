Caching
=======

django CMS REST provides built-in caching support to improve API performance. This guide explains how to configure and use caching effectively.

Overview
--------

Caching in django CMS REST helps reduce database queries and improve response times by storing frequently accessed data in memory or other fast storage systems.

Cache Configuration
------------------

**Basic Configuration:**

.. code-block:: python

    # settings.py
    DJANGOCMS_REST = {
        'CACHE_ENABLED': True,
        'CACHE_TIMEOUT': 300,  # 5 minutes
        'CACHE_KEY_PREFIX': 'djangocms_rest',
    }

**Cache Backend Configuration:**

.. code-block:: python

    # Redis cache (recommended for production)
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

    # Database cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'djangocms_rest_cache',
        }
    }

    # File system cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
        }
    }

Cache Settings
--------------

.. list-table:: Cache Settings
   :header-rows: 1
   :widths: 20 20 20 40

   * - Setting
     - Type
     - Default
     - Description
   * - CACHE_ENABLED
     - boolean
     - True
     - Enable/disable caching
   * - CACHE_TIMEOUT
     - integer
     - 300
     - Cache timeout in seconds
   * - CACHE_KEY_PREFIX
     - string
     - 'djangocms_rest'
     - Prefix for cache keys
   * - CACHE_VERSION
     - integer
     - 1
     - Cache version for invalidation
   * - CACHE_BY_USER
     - boolean
     - False
     - Cache per user
   * - CACHE_BY_LANGUAGE
     - boolean
     - True
     - Cache per language

Cache Keys
----------

django CMS REST uses structured cache keys to organize cached data:

**Page Cache Keys:**

* `djangocms_rest:page:{page_id}:{language}` - Individual page data
* `djangocms_rest:pages:list:{filters_hash}` - Page list with filters
* `djangocms_rest:pages:tree:{language}` - Page tree structure

**Placeholder Cache Keys:**

* `djangocms_rest:placeholder:{placeholder_id}:{language}` - Placeholder data
* `djangocms_rest:placeholders:page:{page_id}:{language}` - Page placeholders

**Plugin Cache Keys:**

* `djangocms_rest:plugin:{plugin_id}:{language}` - Plugin data
* `djangocms_rest:plugins:placeholder:{placeholder_id}:{language}` - Placeholder plugins

Cache Invalidation
-----------------

**Automatic Invalidation:**

django CMS REST automatically invalidates cache when content changes:

.. code-block:: python

    from cms.models import Page
    from djangocms_rest.utils.cache import invalidate_page_cache

    # When a page is updated
    page = Page.objects.get(id=1)
    page.title = "Updated Title"
    page.save()
    
    # Cache is automatically invalidated
    invalidate_page_cache(page)

**Manual Cache Invalidation:**

.. code-block:: python

    from django.core.cache import cache
    from djangocms_rest.utils.cache import (
        invalidate_page_cache,
        invalidate_placeholder_cache,
        invalidate_plugin_cache,
        clear_all_cache
    )

    # Invalidate specific page cache
    page = Page.objects.get(id=1)
    invalidate_page_cache(page)

    # Invalidate placeholder cache
    placeholder = Placeholder.objects.get(id=1)
    invalidate_placeholder_cache(placeholder)

    # Invalidate plugin cache
    plugin = CMSPlugin.objects.get(id=1)
    invalidate_plugin_cache(plugin)

    # Clear all cache
    clear_all_cache()

**Cache Versioning:**

.. code-block:: python

    # Increment cache version to invalidate all cache
    DJANGOCMS_REST = {
        'CACHE_VERSION': 2,  # Increment this to clear all cache
    }

    # Or programmatically
    from django.core.cache import cache
    cache.set('djangocms_rest:version', 2)

Conditional Caching
------------------

**Cache Based on User:**

.. code-block:: python

    DJANGOCMS_REST = {
        'CACHE_BY_USER': True,
    }

**Cache Based on Language:**

.. code-block:: python

    DJANGOCMS_REST = {
        'CACHE_BY_LANGUAGE': True,
    }

**Custom Cache Conditions:**

.. code-block:: python

    from djangocms_rest.utils.cache import get_cache_key

    def custom_cache_key(page, language, user=None):
        base_key = f"page:{page.id}:{language}"
        if user and user.is_staff:
            base_key += f":staff:{user.id}"
        return base_key

    # Use custom cache key
    cache_key = custom_cache_key(page, 'en', user)
    cached_data = cache.get(cache_key) 