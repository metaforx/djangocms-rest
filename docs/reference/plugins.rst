Plugins API
==========

The Plugins API provides endpoints for managing CMS plugins within placeholders.

Endpoints
---------

List Plugins
~~~~~~~~~~~

**GET** ``/api/cms/plugins/``

Retrieve a list of all plugins.

**Query Parameters:**

* ``placeholder`` (integer, optional): Filter by placeholder ID
* ``plugin_type`` (string, optional): Filter by plugin type
* ``language`` (string, optional): Filter by language code
* ``page`` (integer, optional): Page number for pagination (default: 1)
* ``page_size`` (integer, optional): Number of items per page (default: 20, max: 100)

**Example Request:**

.. code-block:: bash

    GET /api/cms/plugins/?plugin_type=TextPlugin

**Example Response:**

.. code-block:: json

    {
        "count": 10,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "plugin_type": "TextPlugin",
                "position": 0,
                "placeholder": 1,
                "body": "<p>Welcome to our website!</p>",
                "created_date": "2024-01-01T00:00:00Z",
                "changed_date": "2024-01-01T00:00:00Z"
            },
            {
                "id": 2,
                "plugin_type": "LinkPlugin",
                "position": 1,
                "placeholder": 1,
                "name": "Learn More",
                "url": "/about/",
                "target": "_self",
                "created_date": "2024-01-01T00:00:00Z",
                "changed_date": "2024-01-01T00:00:00Z"
            }
        ]
    }

Retrieve Plugin
~~~~~~~~~~~~~~

**GET** ``/api/cms/plugins/{id}/``

Retrieve a specific plugin by ID.

**Path Parameters:**

* ``id`` (integer, required): The plugin ID

**Example Request:**

.. code-block:: bash

    GET /api/cms/plugins/1/

**Example Response:**

.. code-block:: json

    {
        "id": 1,
        "plugin_type": "TextPlugin",
        "position": 0,
        "placeholder": 1,
        "body": "<p>Welcome to our website!</p>",
        "created_date": "2024-01-01T00:00:00Z",
        "changed_date": "2024-01-01T00:00:00Z"
    }

Create Plugin
~~~~~~~~~~~~

**POST** ``/api/cms/plugins/``

Create a new plugin.

**Request Body:**

.. code-block:: json

    {
        "plugin_type": "TextPlugin",
        "placeholder": 1,
        "body": "<p>New content here.</p>",
        "position": 0
    }

**Required Fields:**

* ``plugin_type`` (string): Type of plugin (e.g., "TextPlugin", "LinkPlugin")
* ``placeholder`` (integer): Placeholder ID

**Optional Fields:**

* ``position`` (integer): Position within the placeholder
* Plugin-specific fields (e.g., "body" for TextPlugin, "name" and "url" for LinkPlugin)

**Example Response:**

.. code-block:: json

    {
        "id": 3,
        "plugin_type": "TextPlugin",
        "position": 0,
        "placeholder": 1,
        "body": "<p>New content here.</p>",
        "created_date": "2024-01-01T12:00:00Z",
        "changed_date": "2024-01-01T12:00:00Z"
    }

Update Plugin
~~~~~~~~~~~~

**PUT** ``/api/cms/plugins/{id}/``

Update an existing plugin.

**Path Parameters:**

* ``id`` (integer, required): The plugin ID

**Request Body:** Same as Create Plugin

**Example Request:**

.. code-block:: bash

    PUT /api/cms/plugins/1/
    Content-Type: application/json

    {
        "plugin_type": "TextPlugin",
        "placeholder": 1,
        "body": "<p>Updated content here.</p>",
        "position": 0
    }

Partial Update Plugin
~~~~~~~~~~~~~~~~~~~

**PATCH** ``/api/cms/plugins/{id}/``

Partially update a plugin (only specified fields).

**Path Parameters:**

* ``id`` (integer, required): The plugin ID

**Request Body:** Any subset of the plugin fields

**Example Request:**

.. code-block:: bash

    PATCH /api/cms/plugins/1/
    Content-Type: application/json

    {
        "body": "<p>Only update the body content.</p>"
    }

Delete Plugin
~~~~~~~~~~~~

**DELETE** ``/api/cms/plugins/{id}/``

Delete a plugin.

**Path Parameters:**

* ``id`` (integer, required): The plugin ID

**Response:** 204 No Content

Plugin Types
-----------

**TextPlugin:**

.. code-block:: json

    {
        "plugin_type": "TextPlugin",
        "placeholder": 1,
        "body": "<p>HTML content here.</p>"
    }

**LinkPlugin:**

.. code-block:: json

    {
        "plugin_type": "LinkPlugin",
        "placeholder": 1,
        "name": "Click here",
        "url": "/target-page/",
        "target": "_blank",
        "mailto": "",
        "phone": "",
        "anchor": ""
    }

**Custom Plugins:**

For custom plugins, include all required fields for that plugin type:

.. code-block:: json

    {
        "plugin_type": "CustomPlugin",
        "placeholder": 1,
        "custom_field_1": "value1",
        "custom_field_2": "value2"
    }

Field Reference
---------------

.. list-table:: Plugin Fields
   :header-rows: 1
   :widths: 20 20 20 40

   * - Field
     - Type
     - Required
     - Description
   * - id
     - integer
     - No
     - Unique plugin identifier (auto-generated)
   * - plugin_type
     - string
     - Yes
     - Type of plugin (e.g., "TextPlugin", "LinkPlugin")
   * - position
     - integer
     - No
     - Position within the placeholder
   * - placeholder
     - integer
     - Yes
     - Associated placeholder ID
   * - created_date
     - datetime
     - No
     - Creation timestamp (auto-generated)
   * - changed_date
     - datetime
     - No
     - Last modification timestamp (auto-generated)

**TextPlugin Fields:**

.. list-table:: TextPlugin Fields
   :header-rows: 1
   :widths: 20 20 20 40

   * - Field
     - Type
     - Required
     - Description
   * - body
     - string
     - Yes
     - HTML content of the text plugin

**LinkPlugin Fields:**

.. list-table:: LinkPlugin Fields
   :header-rows: 1
   :widths: 20 20 20 40

   * - Field
     - Type
     - Required
     - Description
   * - name
     - string
     - Yes
     - Display text for the link
   * - url
     - string
     - No
     - URL for the link
   * - target
     - string
     - No
     - Link target ("_self", "_blank", etc.)
   * - mailto
     - string
     - No
     - Email address for mailto links
   * - phone
     - string
     - No
     - Phone number for tel links
   * - anchor
     - string
     - No
     - Anchor for page-internal links

Error Handling
--------------

**400 Bad Request:** Invalid data provided

.. code-block:: json

    {
        "plugin_type": ["This field is required."],
        "placeholder": ["Invalid placeholder ID."],
        "body": ["This field is required for TextPlugin."]
    }

**404 Not Found:** Plugin not found

.. code-block:: json

    {
        "detail": "Plugin not found."
    }

**403 Forbidden:** Insufficient permissions

.. code-block:: json

    {
        "detail": "You do not have permission to perform this action."
    }

Examples
--------

**Create a text plugin:**

.. code-block:: python

    import requests

    plugin_data = {
        "plugin_type": "TextPlugin",
        "placeholder": 1,
        "body": "<h1>Welcome</h1><p>This is the main content.</p>"
    }

    response = requests.post(
        'http://localhost:8000/api/cms/plugins/',
        json=plugin_data,
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 201:
        plugin = response.json()
        print(f"Created plugin: {plugin['plugin_type']}")

**Create a link plugin:**

.. code-block:: python

    link_data = {
        "plugin_type": "LinkPlugin",
        "placeholder": 1,
        "name": "Read More",
        "url": "/about/",
        "target": "_self"
    }

    response = requests.post(
        'http://localhost:8000/api/cms/plugins/',
        json=link_data,
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 201:
        link = response.json()
        print(f"Created link: {link['name']} -> {link['url']}")

**Update plugin content:**

.. code-block:: python

    update_data = {
        "plugin_type": "TextPlugin",
        "placeholder": 1,
        "body": "<p>Updated content with new information.</p>"
    }

    response = requests.put(
        'http://localhost:8000/api/cms/plugins/1/',
        json=update_data,
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        print("Plugin updated successfully!")

**Get all plugins in a placeholder:**

.. code-block:: python

    response = requests.get(
        'http://localhost:8000/api/cms/plugins/',
        params={'placeholder': 1},
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        plugins = response.json()
        for plugin in plugins['results']:
            print(f"Plugin {plugin['id']}: {plugin['plugin_type']}")

**Reorder plugins:**

.. code-block:: python

    # Get current plugins
    response = requests.get(
        'http://localhost:8000/api/cms/plugins/',
        params={'placeholder': 1},
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        plugins = response.json()
        
        # Update positions
        for i, plugin in enumerate(plugins['results']):
            update_data = {
                "plugin_type": plugin['plugin_type'],
                "placeholder": plugin['placeholder'],
                "position": i
            }
            
            # Add plugin-specific fields
            if plugin['plugin_type'] == 'TextPlugin':
                update_data['body'] = plugin['body']
            elif plugin['plugin_type'] == 'LinkPlugin':
                update_data['name'] = plugin['name']
                update_data['url'] = plugin['url']
            
            requests.put(
                f'http://localhost:8000/api/cms/plugins/{plugin["id"]}/',
                json=update_data,
                headers={"Authorization": "Token your-token-here"}
            )

**Bulk plugin operations:**

.. code-block:: python

    def create_multiple_plugins(placeholder_id, plugins_data):
        """Create multiple plugins in a placeholder"""
        created_plugins = []
        
        for i, plugin_data in enumerate(plugins_data):
            plugin_data['placeholder'] = placeholder_id
            plugin_data['position'] = i
            
            response = requests.post(
                'http://localhost:8000/api/cms/plugins/',
                json=plugin_data,
                headers={"Authorization": "Token your-token-here"}
            )
            
            if response.status_code == 201:
                created_plugins.append(response.json())
        
        return created_plugins

    # Usage
    plugins_to_create = [
        {
            "plugin_type": "TextPlugin",
            "body": "<h1>Welcome</h1>"
        },
        {
            "plugin_type": "TextPlugin",
            "body": "<p>This is the introduction.</p>"
        },
        {
            "plugin_type": "LinkPlugin",
            "name": "Learn More",
            "url": "/about/"
        }
    ]

    created = create_multiple_plugins(1, plugins_to_create)
    print(f"Created {len(created)} plugins") 