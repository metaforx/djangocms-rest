Pages API
=========

The Pages API provides endpoints for retrieving django CMS pages and their content.

Endpoints
---------

Retrieve Page
~~~~~~~~~~~~

**GET** ``/api/{language}/pages/``

Retrieve a page instance. The page instance includes the placeholders and their links to retrieve dynamic content.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")

**Example Request:**

.. code-block:: bash

    GET /api/en/pages/

**Example Response:**

.. code-block:: json

    {
        "title": "Home",
        "page_title": "Home",
        "menu_title": "Home",
        "meta_description": "Welcome to our website",
        "redirect": null,
        "absolute_url": "/en/",
        "path": "/en/",
        "details": "Welcome to our website",
        "is_home": true,
        "login_required": false,
        "in_navigation": true,
        "soft_root": false,
        "template": "page.html",
        "xframe_options": "SAMEORIGIN",
        "limit_visibility_in_menu": false,
        "language": "en",
        "languages": ["en"],
        "is_preview": false,
        "application_namespace": null,
        "creation_date": "2024-01-01T00:00:00Z",
        "changed_date": "2024-01-01T00:00:00Z",
        "placeholders": [
            {
                "content_type_id": 1,
                "object_id": 1,
                "slot": "content",
                "details": "/api/en/placeholders/1/1/content/"
            }
        ]
    }

Retrieve Page by Path
~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/{language}/pages/{path}/``

Retrieve a page instance by path. The page instance includes the placeholders and their links to retrieve dynamic content.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")
* ``path`` (string, required): Page path (e.g., "about", "contact")

**Example Request:**

.. code-block:: bash

    GET /api/en/pages/about/

**Example Response:**

.. code-block:: json

    {
        "title": "About Us",
        "page_title": "About Us",
        "menu_title": "About",
        "meta_description": "Learn more about our company",
        "redirect": null,
        "absolute_url": "/en/about/",
        "path": "/en/about/",
        "details": "Learn more about our company",
        "is_home": false,
        "login_required": false,
        "in_navigation": true,
        "soft_root": false,
        "template": "page.html",
        "xframe_options": "SAMEORIGIN",
        "limit_visibility_in_menu": false,
        "language": "en",
        "languages": ["en"],
        "is_preview": false,
        "application_namespace": null,
        "creation_date": "2024-01-01T00:00:00Z",
        "changed_date": "2024-01-01T00:00:00Z",
        "placeholders": [
            {
                "content_type_id": 1,
                "object_id": 2,
                "slot": "content",
                "details": "/api/en/placeholders/1/2/content/"
            }
        ]
    }

List Pages
~~~~~~~~~~

**GET** ``/api/{language}/pages-list/``

This is a base class for all list API views. It supports default pagination and sets the allowed methods to GET and OPTIONS.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")

**Query Parameters:**

* ``limit`` (integer, optional): Number of results to return per page
* ``offset`` (integer, optional): The initial index from which to return the results

**Example Request:**

.. code-block:: bash

    GET /api/en/pages-list/?limit=10&offset=0

**Example Response:**

.. code-block:: json

    {
        "count": 25,
        "next": "http://example.com/api/en/pages-list/?limit=10&offset=10",
        "previous": null,
        "results": [
            {
                "title": "Home",
                "page_title": "Home",
                "menu_title": "Home",
                "meta_description": "Welcome to our website",
                "redirect": null,
                "absolute_url": "/en/",
                "path": "/en/",
                "details": "Welcome to our website",
                "is_home": true,
                "login_required": false,
                "in_navigation": true,
                "soft_root": false,
                "template": "page.html",
                "xframe_options": "SAMEORIGIN",
                "limit_visibility_in_menu": false,
                "language": "en",
                "languages": ["en"],
                "is_preview": false,
                "application_namespace": null,
                "creation_date": "2024-01-01T00:00:00Z",
                "changed_date": "2024-01-01T00:00:00Z"
            },
            {
                "title": "About Us",
                "page_title": "About Us",
                "menu_title": "About",
                "meta_description": "Learn more about our company",
                "redirect": null,
                "absolute_url": "/en/about/",
                "path": "/en/about/",
                "details": "Learn more about our company",
                "is_home": false,
                "login_required": false,
                "in_navigation": true,
                "soft_root": false,
                "template": "page.html",
                "xframe_options": "SAMEORIGIN",
                "limit_visibility_in_menu": false,
                "language": "en",
                "languages": ["en"],
                "is_preview": false,
                "application_namespace": null,
                "creation_date": "2024-01-01T00:00:00Z",
                "changed_date": "2024-01-01T00:00:00Z"
            }
        ]
    }

Pages Tree
~~~~~~~~~~

**GET** ``/api/{language}/pages-tree/``

List of all pages on this site for a given language.

**Path Parameters:**

* ``language`` (string, required): Language code (e.g., "en", "de")

**Example Request:**

.. code-block:: bash

    GET /api/en/pages-tree/

**Example Response:**

.. code-block:: json

    {
        "title": "Home",
        "page_title": "Home",
        "menu_title": "Home",
        "meta_description": "Welcome to our website",
        "redirect": null,
        "absolute_url": "/en/",
        "path": "/en/",
        "details": "Welcome to our website",
        "is_home": true,
        "login_required": false,
        "in_navigation": true,
        "soft_root": false,
        "template": "page.html",
        "xframe_options": "SAMEORIGIN",
        "limit_visibility_in_menu": false,
        "language": "en",
        "languages": ["en"],
        "is_preview": false,
        "application_namespace": null,
        "creation_date": "2024-01-01T00:00:00Z",
        "changed_date": "2024-01-01T00:00:00Z",
        "children": [
            {
                "title": "About Us",
                "page_title": "About Us",
                "menu_title": "About",
                "meta_description": "Learn more about our company",
                "redirect": null,
                "absolute_url": "/en/about/",
                "path": "/en/about/",
                "details": "Learn more about our company",
                "is_home": false,
                "login_required": false,
                "in_navigation": true,
                "soft_root": false,
                "template": "page.html",
                "xframe_options": "SAMEORIGIN",
                "limit_visibility_in_menu": false,
                "language": "en",
                "languages": ["en"],
                "is_preview": false,
                "application_namespace": null,
                "creation_date": "2024-01-01T00:00:00Z",
                "changed_date": "2024-01-01T00:00:00Z",
                "children": []
            }
        ]
    }

Field Reference
---------------

.. list-table:: Page Fields
   :header-rows: 1
   :widths: 20 20 20 40

   * - Field
     - Type
     - Nullable
     - Description
   * - title
     - string
     - No
     - Page title (max 255 characters)
   * - page_title
     - string
     - No
     - Page title for browser (max 255 characters)
   * - menu_title
     - string
     - No
     - Title displayed in navigation (max 255 characters)
   * - meta_description
     - string
     - No
     - Meta description for SEO
   * - redirect
     - string
     - Yes
     - Redirect URL (max 2048 characters)
   * - absolute_url
     - string
     - No
     - Full URL path (max 200 characters)
   * - path
     - string
     - No
     - Page path (max 200 characters)
   * - details
     - string
     - No
     - Page details/description (max 2048 characters)
   * - is_home
     - boolean
     - No
     - Whether this is the home page
   * - login_required
     - boolean
     - No
     - Whether login is required to view page
   * - in_navigation
     - boolean
     - No
     - Whether page appears in navigation
   * - soft_root
     - boolean
     - No
     - Whether this is a soft root page
   * - template
     - string
     - No
     - Template name (max 100 characters)
   * - xframe_options
     - string
     - No
     - X-Frame-Options header value (max 50 characters)
   * - limit_visibility_in_menu
     - boolean
     - Yes
     - Limit visibility in menu (default: false)
   * - language
     - string
     - No
     - Language code (max 10 characters)
   * - languages
     - array
     - No
     - Available languages for this page
   * - is_preview
     - boolean
     - No
     - Whether this is a preview (default: false)
   * - application_namespace
     - string
     - Yes
     - Application namespace (max 200 characters)
   * - creation_date
     - string (date-time)
     - No
     - Creation timestamp
   * - changed_date
     - string (date-time)
     - No
     - Last modification timestamp
   * - placeholders
     - array
     - No
     - Page placeholders (only in page detail endpoints)
   * - children
     - array
     - No
     - Child pages (only in tree endpoint, default: [])

Error Handling
--------------

**404 Not Found:** Page not found

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

**Get page by language:**

.. code-block:: python

    import requests

    # Get page for English language
    response = requests.get(
        "http://localhost:8080/api/en/pages/",
        headers={"Cookie": "sessionid=your-session-id"}
    )

    if response.status_code == 200:
        page = response.json()
        print(f"Page: {page['title']} - {page['absolute_url']}")

**Get page by path:**

.. code-block:: python

    # Get specific page by path
    response = requests.get(
        "http://localhost:8080/api/en/pages/about/",
        headers={"Cookie": "sessionid=your-session-id"}
    )

    if response.status_code == 200:
        page = response.json()
        print(f"Page: {page['title']} - {page['absolute_url']}")

**Get paginated list of pages:**

.. code-block:: python

    # Get paginated list of pages
    response = requests.get(
        "http://localhost:8080/api/en/pages-list/?limit=10&offset=0",
        headers={"Cookie": "sessionid=your-session-id"}
    )

    if response.status_code == 200:
        pages = response.json()
        print(f"Found {pages['count']} pages")
        for page in pages['results']:
            print(f"Page: {page['title']} - {page['absolute_url']}")

**Get pages tree structure:**

.. code-block:: python

    # Get pages in tree structure
    response = requests.get(
        "http://localhost:8080/api/en/pages-tree/",
        headers={"Cookie": "sessionid=your-session-id"}
    )

    if response.status_code == 200:
        page_tree = response.json()
        print(f"Root page: {page_tree['title']}")
        for child in page_tree['children']:
            print(f"Child page: {child['title']}") 