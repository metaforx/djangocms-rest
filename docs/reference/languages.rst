Languages API
=============

The Languages API provides endpoints for managing and retrieving language information in django CMS.

Endpoints
---------

List Languages
~~~~~~~~~~~~~

**GET** ``/api/cms/languages/``

Retrieve a list of all available languages.

**Query Parameters:**

* ``page`` (integer, optional): Page number for pagination (default: 1)
* ``page_size`` (integer, optional): Number of items per page (default: 20, max: 100)

**Example Request:**

.. code-block:: bash

    GET /api/cms/languages/

**Example Response:**

.. code-block:: json

    {
        "count": 3,
        "next": null,
        "previous": null,
        "results": [
            {
                "code": "en",
                "name": "English",
                "public": true,
                "fallbacks": ["en"],
                "hide_untranslated": true,
                "redirect_on_fallback": true,
                "prefix_default_language": false
            },
            {
                "code": "de",
                "name": "German",
                "public": true,
                "fallbacks": ["en"],
                "hide_untranslated": true,
                "redirect_on_fallback": true,
                "prefix_default_language": false
            },
            {
                "code": "fr",
                "name": "French",
                "public": true,
                "fallbacks": ["en"],
                "hide_untranslated": true,
                "redirect_on_fallback": true,
                "prefix_default_language": false
            }
        ]
    }

Retrieve Language
~~~~~~~~~~~~~~~~

**GET** ``/api/cms/languages/{code}/``

Retrieve a specific language by its code.

**Path Parameters:**

* ``code`` (string, required): The language code (e.g., "en", "de")

**Example Request:**

.. code-block:: bash

    GET /api/cms/languages/en/

**Example Response:**

.. code-block:: json

    {
        "code": "en",
        "name": "English",
        "public": true,
        "fallbacks": ["en"],
        "hide_untranslated": true,
        "redirect_on_fallback": true,
        "prefix_default_language": false
    }

Field Reference
---------------

.. list-table:: Language Fields
   :header-rows: 1
   :widths: 20 20 20 40

   * - Field
     - Type
     - Required
     - Description
   * - code
     - string
     - Yes
     - Language code (e.g., "en", "de", "fr")
   * - name
     - string
     - Yes
     - Human-readable language name
   * - public
     - boolean
     - No
     - Whether the language is publicly available
   * - fallbacks
     - array
     - No
     - List of fallback language codes
   * - hide_untranslated
     - boolean
     - No
     - Whether to hide untranslated content
   * - redirect_on_fallback
     - boolean
     - No
     - Whether to redirect on fallback
   * - prefix_default_language
     - boolean
     - No
     - Whether to prefix URLs for default language

Error Handling
--------------

**404 Not Found:** Language not found

.. code-block:: json

    {
        "detail": "Language not found."
    }

Examples
--------

**Get all languages:**

.. code-block:: python

    import requests

    response = requests.get('http://localhost:8000/api/cms/languages/')
    languages = response.json()
    
    for language in languages['results']:
        print(f"{language['name']} ({language['code']})")

**Get specific language:**

.. code-block:: python

    response = requests.get('http://localhost:8000/api/cms/languages/en/')
    english = response.json()
    print(f"English fallbacks: {english['fallbacks']}")

**Filter pages by language:**

.. code-block:: python

    # Get pages in English
    response = requests.get('http://localhost:8000/api/cms/pages/', params={'language': 'en'})
    english_pages = response.json()
    
    # Get pages in German
    response = requests.get('http://localhost:8000/api/cms/pages/', params={'language': 'de'})
    german_pages = response.json() 