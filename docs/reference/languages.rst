Languages API
=============

The Languages API provides endpoints for retrieving language information in django CMS.

Endpoints
---------

List Languages
~~~~~~~~~~~~~

**GET** ``/api/languages/``

List of languages available for the site.

**Example Request:**

.. code-block:: bash

    GET /api/languages/

**Example Response:**

.. code-block:: json

    {
        "code": "en",
        "name": "English",
        "public": true,
        "fallbacks": ["en"],
        "redirect_on_fallback": true,
        "hide_untranslated": true
    }

Field Reference
---------------

.. list-table:: Language Fields
   :header-rows: 1
   :widths: 20 20 20 40

   * - Field
     - Type
     - Nullable
     - Description
   * - code
     - string
     - No
     - Language code (max 10 characters)
   * - name
     - string
     - No
     - Human-readable language name (max 100 characters)
   * - public
     - boolean
     - No
     - Whether the language is publicly available
   * - fallbacks
     - array
     - No
     - List of fallback language codes (max 10 characters each)
   * - redirect_on_fallback
     - boolean
     - No
     - Whether to redirect on fallback
   * - hide_untranslated
     - boolean
     - No
     - Whether to hide untranslated content

Error Handling
--------------

**404 Not Found:** Language not found

.. code-block:: json

    {
        "detail": "Not found."
    }

**403 Forbidden:** Insufficient permissions

.. code-block:: json

    {
        "detail": "You do not have permission to perform this action."
    }

Examples
--------

**Get languages:**

.. code-block:: python

    import requests

    # Get languages (no authentication required)
    response = requests.get('http://localhost:8080/api/languages/')
    
    if response.status_code == 200:
        language = response.json()
        print(f"Language: {language['name']} ({language['code']})")
        print(f"Fallbacks: {language['fallbacks']}")
        print(f"Public: {language['public']}")

**Get languages with authentication:**

.. code-block:: python

    # Get languages with session authentication
    response = requests.get(
        'http://localhost:8080/api/languages/',
        headers={"Cookie": "sessionid=your-session-id"}
    )
    
    if response.status_code == 200:
        language = response.json()
        print(f"Language: {language['name']} ({language['code']})")
        print(f"Hide untranslated: {language['hide_untranslated']}")
        print(f"Redirect on fallback: {language['redirect_on_fallback']}") 