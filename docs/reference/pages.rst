Pages API
=========

The Pages API provides endpoints for managing django CMS pages, including creating, reading, updating, and deleting pages.

Endpoints
---------

List Pages
~~~~~~~~~~

**GET** ``/api/cms/pages/``

Retrieve a list of all pages.

**Query Parameters:**

* ``language`` (string, optional): Filter by language code (e.g., "en", "de")
* ``is_published`` (boolean, optional): Filter by publication status
* ``template`` (string, optional): Filter by template name
* ``parent`` (integer, optional): Filter by parent page ID
* ``page`` (integer, optional): Page number for pagination (default: 1)
* ``page_size`` (integer, optional): Number of items per page (default: 20, max: 100)

**Example Request:**

.. code-block:: bash

    GET /api/cms/pages/?language=en&is_published=true&page=1&page_size=10

**Example Response:**

.. code-block:: json

    {
        "count": 25,
        "next": "http://example.com/api/cms/pages/?page=2&page_size=10",
        "previous": null,
        "results": [
            {
                "id": 1,
                "title": "Home",
                "slug": "home",
                "language": "en",
                "template": "page.html",
                "is_published": true,
                "is_home": true,
                "parent": null,
                "created_date": "2024-01-01T00:00:00Z",
                "changed_date": "2024-01-01T00:00:00Z",
                "publication_date": "2024-01-01T00:00:00Z",
                "publication_end_date": null,
                "url": "/home/"
            },
            {
                "id": 2,
                "title": "About",
                "slug": "about",
                "language": "en",
                "template": "page.html",
                "is_published": true,
                "is_home": false,
                "parent": 1,
                "created_date": "2024-01-01T00:00:00Z",
                "changed_date": "2024-01-01T00:00:00Z",
                "publication_date": "2024-01-01T00:00:00Z",
                "publication_end_date": null,
                "url": "/home/about/"
            }
        ]
    }

Retrieve Page
~~~~~~~~~~~~

**GET** ``/api/cms/pages/{id}/``

Retrieve a specific page by ID.

**Path Parameters:**

* ``id`` (integer, required): The page ID

**Example Request:**

.. code-block:: bash

    GET /api/cms/pages/1/

**Example Response:**

.. code-block:: json

    {
        "id": 1,
        "title": "Home",
        "slug": "home",
        "language": "en",
        "template": "page.html",
        "is_published": true,
        "is_home": true,
        "parent": null,
        "created_date": "2024-01-01T00:00:00Z",
        "changed_date": "2024-01-01T00:00:00Z",
        "publication_date": "2024-01-01T00:00:00Z",
        "publication_end_date": null,
        "url": "/home/",
        "meta_description": "Welcome to our website",
        "meta_keywords": "home, welcome",
        "meta_title": "Home - Our Website"
    }

Create Page
~~~~~~~~~~~

**POST** ``/api/cms/pages/``

Create a new page.

**Request Body:**

.. code-block:: json

    {
        "title": "New Page",
        "slug": "new-page",
        "language": "en",
        "template": "page.html",
        "is_published": false,
        "parent": null,
        "meta_description": "Description for SEO",
        "meta_keywords": "keyword1, keyword2",
        "meta_title": "Custom Page Title"
    }

**Required Fields:**

* ``title`` (string): Page title
* ``slug`` (string): URL slug (must be unique within the same parent and language)
* ``language`` (string): Language code
* ``template`` (string): Template name

**Optional Fields:**

* ``is_published`` (boolean): Publication status (default: false)
* ``parent`` (integer): Parent page ID (default: null for root pages)
* ``meta_description`` (string): Meta description for SEO
* ``meta_keywords`` (string): Meta keywords for SEO
* ``meta_title`` (string): Custom meta title

**Example Response:**

.. code-block:: json

    {
        "id": 3,
        "title": "New Page",
        "slug": "new-page",
        "language": "en",
        "template": "page.html",
        "is_published": false,
        "is_home": false,
        "parent": null,
        "created_date": "2024-01-01T12:00:00Z",
        "changed_date": "2024-01-01T12:00:00Z",
        "publication_date": null,
        "publication_end_date": null,
        "url": "/new-page/",
        "meta_description": "Description for SEO",
        "meta_keywords": "keyword1, keyword2",
        "meta_title": "Custom Page Title"
    }

Update Page
~~~~~~~~~~~

**PUT** ``/api/cms/pages/{id}/``

Update an existing page.

**Path Parameters:**

* ``id`` (integer, required): The page ID

**Request Body:** Same as Create Page

**Example Request:**

.. code-block:: bash

    PUT /api/cms/pages/3/
    Content-Type: application/json

    {
        "title": "Updated Page Title",
        "slug": "updated-page",
        "language": "en",
        "template": "page.html",
        "is_published": true,
        "meta_description": "Updated description"
    }

**Example Response:**

.. code-block:: json

    {
        "id": 3,
        "title": "Updated Page Title",
        "slug": "updated-page",
        "language": "en",
        "template": "page.html",
        "is_published": true,
        "is_home": false,
        "parent": null,
        "created_date": "2024-01-01T12:00:00Z",
        "changed_date": "2024-01-01T13:00:00Z",
        "publication_date": "2024-01-01T13:00:00Z",
        "publication_end_date": null,
        "url": "/updated-page/",
        "meta_description": "Updated description",
        "meta_keywords": "keyword1, keyword2",
        "meta_title": "Custom Page Title"
    }

Partial Update Page
~~~~~~~~~~~~~~~~~~

**PATCH** ``/api/cms/pages/{id}/``

Partially update a page (only specified fields).

**Path Parameters:**

* ``id`` (integer, required): The page ID

**Request Body:** Any subset of the page fields

**Example Request:**

.. code-block:: bash

    PATCH /api/cms/pages/3/
    Content-Type: application/json

    {
        "title": "New Title",
        "is_published": true
    }

Delete Page
~~~~~~~~~~~

**DELETE** ``/api/cms/pages/{id}/``

Delete a page.

**Path Parameters:**

* ``id`` (integer, required): The page ID

**Example Request:**

.. code-block:: bash

    DELETE /api/cms/pages/3/

**Response:** 204 No Content

Page Tree
~~~~~~~~~

**GET** ``/api/cms/pages/tree/``

Retrieve the page hierarchy as a tree structure.

**Query Parameters:**

* ``language`` (string, optional): Filter by language code
* ``is_published`` (boolean, optional): Filter by publication status

**Example Response:**

.. code-block:: json

    {
        "count": 3,
        "results": [
            {
                "id": 1,
                "title": "Home",
                "slug": "home",
                "language": "en",
                "is_published": true,
                "url": "/home/",
                "children": [
                    {
                        "id": 2,
                        "title": "About",
                        "slug": "about",
                        "language": "en",
                        "is_published": true,
                        "url": "/home/about/",
                        "children": []
                    }
                ]
            }
        ]
    }

Page Root
~~~~~~~~~

**GET** ``/api/cms/pages/root/``

Retrieve the root page (home page).

**Query Parameters:**

* ``language`` (string, optional): Language code (default: site default)

**Example Response:**

.. code-block:: json

    {
        "id": 1,
        "title": "Home",
        "slug": "home",
        "language": "en",
        "template": "page.html",
        "is_published": true,
        "is_home": true,
        "parent": null,
        "created_date": "2024-01-01T00:00:00Z",
        "changed_date": "2024-01-01T00:00:00Z",
        "publication_date": "2024-01-01T00:00:00Z",
        "publication_end_date": null,
        "url": "/home/"
    }

Field Reference
---------------

.. list-table:: Page Fields
   :header-rows: 1
   :widths: 20 20 20 40

   * - Field
     - Type
     - Required
     - Description
   * - id
     - integer
     - No
     - Unique page identifier (auto-generated)
   * - title
     - string
     - Yes
     - Page title
   * - slug
     - string
     - Yes
     - URL slug (must be unique within parent and language)
   * - language
     - string
     - Yes
     - Language code (e.g., "en", "de")
   * - template
     - string
     - Yes
     - Template name from CMS_TEMPLATES setting
   * - is_published
     - boolean
     - No
     - Publication status (default: false)
   * - is_home
     - boolean
     - No
     - Whether this is the home page (auto-determined)
   * - parent
     - integer
     - No
     - Parent page ID (null for root pages)
   * - created_date
     - datetime
     - No
     - Creation timestamp (auto-generated)
   * - changed_date
     - datetime
     - No
     - Last modification timestamp (auto-generated)
   * - publication_date
     - datetime
     - No
     - Publication date (set when is_published becomes true)
   * - publication_end_date
     - datetime
     - No
     - End of publication date
   * - url
     - string
     - No
     - Full URL path (auto-generated)
   * - meta_description
     - string
     - No
     - Meta description for SEO
   * - meta_keywords
     - string
     - No
     - Meta keywords for SEO
   * - meta_title
     - string
     - No
     - Custom meta title

Error Handling
--------------

**400 Bad Request:** Invalid data provided

.. code-block:: json

    {
        "title": ["This field is required."],
        "slug": ["A page with this slug already exists."]
    }

**404 Not Found:** Page not found

.. code-block:: json

    {
        "detail": "Page not found."
    }

**403 Forbidden:** Insufficient permissions

.. code-block:: json

    {
        "detail": "You do not have permission to perform this action."
    }

Examples
--------

**Create a page with content:**

.. code-block:: python

    import requests

    # Create a new page
    page_data = {
        "title": "Contact Us",
        "slug": "contact",
        "language": "en",
        "template": "page.html",
        "is_published": True,
        "meta_description": "Get in touch with us"
    }

    response = requests.post(
        "http://localhost:8000/api/cms/pages/",
        json=page_data,
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 201:
        page = response.json()
        print(f"Created page: {page['title']}")

**Get published pages in English:**

.. code-block:: python

    response = requests.get(
        "http://localhost:8000/api/cms/pages/",
        params={"language": "en", "is_published": True},
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        pages = response.json()
        for page in pages['results']:
            print(f"Page: {page['title']} - {page['url']}")

**Update page publication status:**

.. code-block:: python

    response = requests.patch(
        "http://localhost:8000/api/cms/pages/1/",
        json={"is_published": True},
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        print("Page published successfully") 