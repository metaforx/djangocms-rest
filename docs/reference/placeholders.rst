Placeholders API
===============

The Placeholders API provides endpoints for managing page placeholders and their content in django CMS.

Endpoints
---------

List Placeholders
~~~~~~~~~~~~~~~~

**GET** ``/api/cms/placeholders/``

Retrieve a list of all placeholders.

**Query Parameters:**

* ``page`` (integer, optional): Filter by page ID
* ``slot`` (string, optional): Filter by placeholder slot name
* ``language`` (string, optional): Filter by language code
* ``page`` (integer, optional): Page number for pagination (default: 1)
* ``page_size`` (integer, optional): Number of items per page (default: 20, max: 100)

**Example Request:**

.. code-block:: bash

    GET /api/cms/placeholders/?page=1&slot=content

**Example Response:**

.. code-block:: json

    {
        "count": 5,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "slot": "content",
                "page": 1,
                "language": "en",
                "plugin_count": 3,
                "plugins": [
                    {
                        "id": 1,
                        "plugin_type": "TextPlugin",
                        "position": 0,
                        "body": "<p>Welcome to our website!</p>"
                    }
                ]
            }
        ]
    }

Retrieve Placeholder
~~~~~~~~~~~~~~~~~~

**GET** ``/api/cms/placeholders/{id}/``

Retrieve a specific placeholder by ID.

**Path Parameters:**

* ``id`` (integer, required): The placeholder ID

**Example Request:**

.. code-block:: bash

    GET /api/cms/placeholders/1/

**Example Response:**

.. code-block:: json

    {
        "id": 1,
        "slot": "content",
        "page": 1,
        "language": "en",
        "plugin_count": 3,
        "plugins": [
            {
                "id": 1,
                "plugin_type": "TextPlugin",
                "position": 0,
                "body": "<p>Welcome to our website!</p>"
            },
            {
                "id": 2,
                "plugin_type": "LinkPlugin",
                "position": 1,
                "name": "Learn More",
                "url": "/about/"
            }
        ]
    }

Create Placeholder
~~~~~~~~~~~~~~~~~

**POST** ``/api/cms/placeholders/``

Create a new placeholder.

**Request Body:**

.. code-block:: json

    {
        "slot": "content",
        "page": 1,
        "language": "en"
    }

**Required Fields:**

* ``slot`` (string): Placeholder slot name
* ``page`` (integer): Page ID
* ``language`` (string): Language code

**Example Response:**

.. code-block:: json

    {
        "id": 2,
        "slot": "sidebar",
        "page": 1,
        "language": "en",
        "plugin_count": 0,
        "plugins": []
    }

Update Placeholder
~~~~~~~~~~~~~~~~~

**PUT** ``/api/cms/placeholders/{id}/``

Update an existing placeholder.

**Path Parameters:**

* ``id`` (integer, required): The placeholder ID

**Request Body:** Same as Create Placeholder

Delete Placeholder
~~~~~~~~~~~~~~~~~

**DELETE** ``/api/cms/placeholders/{id}/``

Delete a placeholder.

**Path Parameters:**

* ``id`` (integer, required): The placeholder ID

**Response:** 204 No Content

Page Placeholders
~~~~~~~~~~~~~~~~

**GET** ``/api/cms/pages/{page_id}/placeholders/``

Retrieve all placeholders for a specific page.

**Path Parameters:**

* ``page_id`` (integer, required): The page ID

**Query Parameters:**

* ``language`` (string, optional): Filter by language code
* ``slot`` (string, optional): Filter by placeholder slot name

**Example Request:**

.. code-block:: bash

    GET /api/cms/pages/1/placeholders/?language=en

**Example Response:**

.. code-block:: json

    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "slot": "content",
                "page": 1,
                "language": "en",
                "plugin_count": 3,
                "plugins": [...]
            },
            {
                "id": 2,
                "slot": "sidebar",
                "page": 1,
                "language": "en",
                "plugin_count": 1,
                "plugins": [...]
            }
        ]
    }

Plugin Management
----------------

Add Plugin to Placeholder
~~~~~~~~~~~~~~~~~~~~~~~~

**POST** ``/api/cms/placeholders/{id}/plugins/``

Add a plugin to a placeholder.

**Path Parameters:**

* ``id`` (integer, required): The placeholder ID

**Request Body:**

.. code-block:: json

    {
        "plugin_type": "TextPlugin",
        "body": "<p>This is new content.</p>",
        "position": 0
    }

**Example Response:**

.. code-block:: json

    {
        "id": 3,
        "plugin_type": "TextPlugin",
        "position": 0,
        "body": "<p>This is new content.</p>",
        "placeholder": 1
    }

List Plugins in Placeholder
~~~~~~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/cms/placeholders/{id}/plugins/``

Retrieve all plugins in a placeholder.

**Path Parameters:**

* ``id`` (integer, required): The placeholder ID

**Example Response:**

.. code-block:: json

    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "plugin_type": "TextPlugin",
                "position": 0,
                "body": "<p>First plugin content.</p>"
            },
            {
                "id": 2,
                "plugin_type": "LinkPlugin",
                "position": 1,
                "name": "Learn More",
                "url": "/about/"
            }
        ]
    }

Field Reference
---------------

.. list-table:: Placeholder Fields
   :header-rows: 1
   :widths: 20 20 20 40

   * - Field
     - Type
     - Required
     - Description
   * - id
     - integer
     - No
     - Unique placeholder identifier (auto-generated)
   * - slot
     - string
     - Yes
     - Placeholder slot name (e.g., "content", "sidebar")
   * - page
     - integer
     - Yes
     - Associated page ID
   * - language
     - string
     - Yes
     - Language code
   * - plugin_count
     - integer
     - No
     - Number of plugins in the placeholder
   * - plugins
     - array
     - No
     - List of plugins in the placeholder

Error Handling
--------------

**400 Bad Request:** Invalid data provided

.. code-block:: json

    {
        "slot": ["This field is required."],
        "page": ["Invalid page ID."]
    }

**404 Not Found:** Placeholder not found

.. code-block:: json

    {
        "detail": "Placeholder not found."
    }

**403 Forbidden:** Insufficient permissions

.. code-block:: json

    {
        "detail": "You do not have permission to perform this action."
    }

Examples
--------

**Create a placeholder and add content:**

.. code-block:: python

    import requests

    # Create a placeholder
    placeholder_data = {
        "slot": "content",
        "page": 1,
        "language": "en"
    }

    response = requests.post(
        'http://localhost:8000/api/cms/placeholders/',
        json=placeholder_data,
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 201:
        placeholder = response.json()
        
        # Add a text plugin
        plugin_data = {
            "plugin_type": "TextPlugin",
            "body": "<p>Welcome to our website!</p>"
        }
        
        plugin_response = requests.post(
            f'http://localhost:8000/api/cms/placeholders/{placeholder["id"]}/plugins/',
            json=plugin_data,
            headers={"Authorization": "Token your-token-here"}
        )
        
        if plugin_response.status_code == 201:
            print("Content added successfully!")

**Get all placeholders for a page:**

.. code-block:: python

    response = requests.get(
        'http://localhost:8000/api/cms/pages/1/placeholders/',
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        placeholders = response.json()
        for placeholder in placeholders['results']:
            print(f"Placeholder: {placeholder['slot']} ({placeholder['plugin_count']} plugins)")

**Add multiple plugins to a placeholder:**

.. code-block:: python

    placeholder_id = 1
    plugins = [
        {
            "plugin_type": "TextPlugin",
            "body": "<h1>Welcome</h1><p>This is the main content.</p>"
        },
        {
            "plugin_type": "LinkPlugin",
            "name": "Read More",
            "url": "/about/"
        }
    ]

    for plugin_data in plugins:
        response = requests.post(
            f'http://localhost:8000/api/cms/placeholders/{placeholder_id}/plugins/',
            json=plugin_data,
            headers={"Authorization": "Token your-token-here"}
        )
        
        if response.status_code == 201:
            print(f"Added {plugin_data['plugin_type']}")

**Update placeholder content:**

.. code-block:: python

    # Get current plugins
    response = requests.get(
        'http://localhost:8000/api/cms/placeholders/1/plugins/',
        headers={"Authorization": "Token your-token-here"}
    )
    
    if response.status_code == 200:
        plugins = response.json()
        
        # Update first plugin
        if plugins['results']:
            plugin = plugins['results'][0]
            updated_data = {
                "plugin_type": plugin['plugin_type'],
                "body": "<p>Updated content!</p>"
            }
            
            update_response = requests.put(
                f'http://localhost:8000/api/cms/plugins/{plugin["id"]}/',
                json=updated_data,
                headers={"Authorization": "Token your-token-here"}
            )
            
            if update_response.status_code == 200:
                print("Plugin updated successfully!") 