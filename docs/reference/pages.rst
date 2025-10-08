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

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/pages/?preview=true

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

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/pages/about/?preview=true

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
* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/pages-list/?limit=10&offset=0&preview=true

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

**Query Parameters:**

* ``preview`` (boolean, optional): Set to true to preview unpublished content (admin access required)

**Example Request:**

.. code-block:: bash

    GET /api/en/pages-tree/?preview=true

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
