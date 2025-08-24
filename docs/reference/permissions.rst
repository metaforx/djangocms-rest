Permissions API
==============

The Permissions API provides endpoints for managing and checking permissions in django CMS REST.

Endpoints
---------

List Permissions
~~~~~~~~~~~~~~~

**GET** ``/api/cms/permissions/``

Retrieve a list of all available permissions.

**Query Parameters:**

* ``user`` (integer, optional): Filter by user ID
* ``model`` (string, optional): Filter by model name
* ``action`` (string, optional): Filter by action (add, change, delete, view)
* ``page`` (integer, optional): Page number for pagination (default: 1)
* ``page_size`` (integer, optional): Number of items per page (default: 20, max: 100)

**Example Request:**

.. code-block:: bash

    GET /api/cms/permissions/?user=1&model=page

**Example Response:**

.. code-block:: json

    {
        "count": 4,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "Can add page",
                "codename": "add_page",
                "content_type": "page",
                "user": 1,
                "has_permission": true
            },
            {
                "id": 2,
                "name": "Can change page",
                "codename": "change_page",
                "content_type": "page",
                "user": 1,
                "has_permission": true
            },
            {
                "id": 3,
                "name": "Can delete page",
                "codename": "delete_page",
                "content_type": "page",
                "user": 1,
                "has_permission": false
            },
            {
                "id": 4,
                "name": "Can view page",
                "codename": "view_page",
                "content_type": "page",
                "user": 1,
                "has_permission": true
            }
        ]
    }

Check User Permissions
~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/cms/permissions/check/``

Check if the current user has specific permissions.

**Query Parameters:**

* ``permissions`` (string, required): Comma-separated list of permission codenames
* ``object_id`` (integer, optional): Object ID for object-level permissions

**Example Request:**

.. code-block:: bash

    GET /api/cms/permissions/check/?permissions=add_page,change_page&object_id=1

**Example Response:**

.. code-block:: json

    {
        "user": 1,
        "permissions": {
            "add_page": true,
            "change_page": true,
            "delete_page": false,
            "view_page": true
        },
        "object_permissions": {
            "1": {
                "change_page": true,
                "delete_page": false
            }
        }
    }

User Permissions
~~~~~~~~~~~~~~~

**GET** ``/api/cms/permissions/user/{user_id}/``

Retrieve all permissions for a specific user.

**Path Parameters:**

* ``user_id`` (integer, required): The user ID

**Query Parameters:**

* ``model`` (string, optional): Filter by model name
* ``action`` (string, optional): Filter by action

**Example Request:**

.. code-block:: bash

    GET /api/cms/permissions/user/1/?model=page

**Example Response:**

.. code-block:: json

    {
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "is_staff": true,
            "is_superuser": true
        },
        "permissions": [
            {
                "id": 1,
                "name": "Can add page",
                "codename": "add_page",
                "content_type": "page",
                "has_permission": true
            },
            {
                "id": 2,
                "name": "Can change page",
                "codename": "change_page",
                "content_type": "page",
                "has_permission": true
            }
        ],
        "groups": [
            {
                "id": 1,
                "name": "Content Editors",
                "permissions": [
                    {
                        "id": 1,
                        "name": "Can add page",
                        "codename": "add_page",
                        "content_type": "page"
                    }
                ]
            }
        ]
    }

Grant Permission
~~~~~~~~~~~~~~~

**POST** ``/api/cms/permissions/grant/``

Grant a permission to a user.

**Request Body:**

.. code-block:: json

    {
        "user": 1,
        "permission": "add_page",
        "content_type": "page"
    }

**Required Fields:**

* ``user`` (integer): User ID
* ``permission`` (string): Permission codename
* ``content_type`` (string): Content type name

**Example Response:**

.. code-block:: json

    {
        "success": true,
        "message": "Permission granted successfully",
        "permission": {
            "id": 1,
            "name": "Can add page",
            "codename": "add_page",
            "content_type": "page",
            "user": 1
        }
    }

Revoke Permission
~~~~~~~~~~~~~~~~

**POST** ``/api/cms/permissions/revoke/``

Revoke a permission from a user.

**Request Body:**

.. code-block:: json

    {
        "user": 1,
        "permission": "delete_page",
        "content_type": "page"
    }

**Required Fields:**

* ``user`` (integer): User ID
* ``permission`` (string): Permission codename
* ``content_type`` (string): Content type name

**Example Response:**

.. code-block:: json

    {
        "success": true,
        "message": "Permission revoked successfully"
    }

Available Permissions
--------------------

**Page Permissions:**

* ``add_page`` - Create new pages
* ``change_page`` - Edit existing pages
* ``delete_page`` - Delete pages
* ``view_page`` - View pages

**Placeholder Permissions:**

* ``add_placeholder`` - Create new placeholders
* ``change_placeholder`` - Edit placeholders
* ``delete_placeholder`` - Delete placeholders
* ``view_placeholder`` - View placeholders

**Plugin Permissions:**

* ``add_cmsplugin`` - Add plugins to placeholders
* ``change_cmsplugin`` - Edit plugins
* ``delete_cmsplugin`` - Delete plugins
* ``view_cmsplugin`` - View plugins

**Language Permissions:**

* ``add_language`` - Add new languages
* ``change_language`` - Edit language settings
* ``delete_language`` - Delete languages
* ``view_language`` - View languages

Field Reference
---------------

.. list-table:: Permission Fields
   :header-rows: 1
   :widths: 20 20 20 40

   * - Field
     - Type
     - Required
     - Description
   * - id
     - integer
     - No
     - Unique permission identifier
   * - name
     - string
     - Yes
     - Human-readable permission name
   * - codename
     - string
     - Yes
     - Permission codename
   * - content_type
     - string
     - Yes
     - Content type name
   * - user
     - integer
     - No
     - Associated user ID
   * - has_permission
     - boolean
     - No
     - Whether user has this permission

Error Handling
--------------

**400 Bad Request:** Invalid data provided

.. code-block:: json

    {
        "user": ["Invalid user ID."],
        "permission": ["Invalid permission codename."]
    }

**403 Forbidden:** Insufficient permissions

.. code-block:: json

    {
        "detail": "You do not have permission to manage permissions."
    }

**404 Not Found:** User or permission not found

.. code-block:: json

    {
        "detail": "User not found."
    }

Examples
--------

**Check current user permissions:**

.. code-block:: python

    import requests

    response = requests.get(
        'http://localhost:8000/api/cms/permissions/check/',
        params={'permissions': 'add_page,change_page,delete_page'},
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        permissions = response.json()
        for perm, has_perm in permissions['permissions'].items():
            print(f"{perm}: {'Yes' if has_perm else 'No'}")

**Get user permissions:**

.. code-block:: python

    response = requests.get(
        'http://localhost:8000/api/cms/permissions/user/1/',
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        user_perms = response.json()
        print(f"User: {user_perms['user']['username']}")
        for perm in user_perms['permissions']:
            print(f"- {perm['name']}: {perm['has_permission']}")

**Grant permission to user:**

.. code-block:: python

    grant_data = {
        "user": 2,
        "permission": "add_page",
        "content_type": "page"
    }

    response = requests.post(
        'http://localhost:8000/api/cms/permissions/grant/',
        json=grant_data,
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        result = response.json()
        print(result['message'])

**Revoke permission from user:**

.. code-block:: python

    revoke_data = {
        "user": 2,
        "permission": "delete_page",
        "content_type": "page"
    }

    response = requests.post(
        'http://localhost:8000/api/cms/permissions/revoke/',
        json=revoke_data,
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        result = response.json()
        print(result['message'])

**Check object-level permissions:**

.. code-block:: python

    response = requests.get(
        'http://localhost:8000/api/cms/permissions/check/',
        params={
            'permissions': 'change_page,delete_page',
            'object_id': 1
        },
        headers={"Authorization": "Token your-token-here"}
    )

    if response.status_code == 200:
        permissions = response.json()
        object_perms = permissions.get('object_permissions', {}).get('1', {})
        for perm, has_perm in object_perms.items():
            print(f"Page 1 - {perm}: {'Yes' if has_perm else 'No'}")

**Permission management utility:**

.. code-block:: python

    class PermissionManager:
        def __init__(self, base_url, token):
            self.base_url = base_url
            self.headers = {"Authorization": f"Token {token}"}
        
        def check_permissions(self, permissions, object_id=None):
            """Check if current user has specified permissions"""
            params = {'permissions': ','.join(permissions)}
            if object_id:
                params['object_id'] = object_id
            
            response = requests.get(
                f'{self.base_url}/api/cms/permissions/check/',
                params=params,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        
        def grant_permission(self, user_id, permission, content_type):
            """Grant permission to user"""
            data = {
                'user': user_id,
                'permission': permission,
                'content_type': content_type
            }
            
            response = requests.post(
                f'{self.base_url}/api/cms/permissions/grant/',
                json=data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        
        def revoke_permission(self, user_id, permission, content_type):
            """Revoke permission from user"""
            data = {
                'user': user_id,
                'permission': permission,
                'content_type': content_type
            }
            
            response = requests.post(
                f'{self.base_url}/api/cms/permissions/revoke/',
                json=data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    # Usage
    perm_manager = PermissionManager('http://localhost:8000', 'your-token-here')
    
    # Check permissions
    perms = perm_manager.check_permissions(['add_page', 'change_page'])
    print(f"Can add pages: {perms['permissions']['add_page']}")
    
    # Grant permission
    result = perm_manager.grant_permission(2, 'add_page', 'page')
    print(result['message']) 