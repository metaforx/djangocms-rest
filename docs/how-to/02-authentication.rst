Authentication
==============

djangocms-rest uses **Session Authentication** as the only authentication method. This means that users must be logged into the Django CMS admin interface to access protected API endpoints.

Overview
--------

djangocms-rest is designed to work seamlessly with the existing Django CMS admin interface. The API respects the same authentication and permissions as the admin interface, ensuring a consistent user experience.

**Key Points:**

* Users must be logged into Django CMS admin to access protected API endpoints
* The API uses the same session-based authentication as the admin interface
* All permissions are inherited from the Django CMS permission system
* No additional authentication setup is required beyond the standard Django CMS installation

Session Authentication
---------------------

Session authentication is the default and only authentication method for djangocms-rest.

**Configuration:**

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    }

**How It Works:**

1. **User logs into Django CMS admin** at `/admin/`
2. **Session is established** and stored in the database
3. **API requests use the same session** to authenticate the user
4. **Permissions are checked** using Django's built-in permission system

**Usage Examples:**

**Python Client:**

.. code-block:: python

    import requests

    # Create a session
    session = requests.Session()
    
    # Login to Django admin
    login_response = session.post('http://localhost:8000/admin/login/', data={
        'username': 'admin',
        'password': 'password',
        'csrfmiddlewaretoken': 'your-csrf-token'
    })
    
    # Make API requests using the same session
    response = session.get('http://localhost:8000/api/cms/pages/')
    print(response.json())

**JavaScript Client:**

.. code-block:: javascript

    // First, login to Django admin
    fetch('/admin/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'username=admin&password=password&csrfmiddlewaretoken=your-csrf-token',
        credentials: 'include'  // Important: include cookies
    })
    .then(() => {
        // Now make API requests
        return fetch('/api/cms/pages/', {
            credentials: 'include'  // Include session cookies
        });
    })
    .then(response => response.json())
    .then(data => console.log(data));

**cURL Example:**

.. code-block:: bash

    # First, login and save cookies
    curl -c cookies.txt -X POST http://localhost:8000/admin/login/ \
         -d "username=admin&password=password&csrfmiddlewaretoken=your-csrf-token"
    
    # Then use the cookies for API requests
    curl -b cookies.txt http://localhost:8000/api/cms/pages/

Permission System
----------------

djangocms-rest uses Django's built-in permission system. The same permissions that control access in the Django CMS admin interface also control access to the API endpoints.

**Default Permissions:**

* **Pages API:**
  * `cms.add_page` - Create new pages
  * `cms.change_page` - Update existing pages
  * `cms.delete_page` - Delete pages
  * `cms.view_page` - View pages

* **Placeholders API:**
  * `cms.add_placeholder` - Add placeholders
  * `cms.change_placeholder` - Modify placeholders
  * `cms.delete_placeholder` - Delete placeholders
  * `cms.view_placeholder` - View placeholders

* **Plugins API:**
  * `cms.add_cmsplugin` - Add plugins
  * `cms.change_cmsplugin` - Modify plugins
  * `cms.delete_cmsplugin` - Delete plugins
  * `cms.view_cmsplugin` - View plugins

**Available Permission Classes:**

* ``IsAuthenticated``: Require authentication for all requests
* ``IsAdminUser``: Require admin user for all requests
* ``AllowAny``: Allow all requests (no authentication required)
* ``IsAuthenticatedOrReadOnly``: Require authentication for write operations

Anonymous Access
---------------

By default, djangocms-rest requires authentication for all endpoints. However, you can configure it to allow anonymous access for read operations:

.. code-block:: python

    # settings.py
    DJANGOCMS_REST = {
        'ALLOW_ANONYMOUS_READ': True,
        'REQUIRE_AUTHENTICATION': False,
    }

Security Best Practices
----------------------

1. **Use HTTPS in Production:**

.. code-block:: python

    # settings.py
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

2. **Set Secure Headers:**

.. code-block:: python

    # settings.py
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

3. **Configure CORS (if needed):**

.. code-block:: bash

    pip install django-cors-headers

.. code-block:: python

    INSTALLED_APPS = [
        # ... other apps
        'corsheaders',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        # ... other middleware
    ]

    CORS_ALLOWED_ORIGINS = [
        "https://example.com",
        "https://sub.example.com",
    ]

Testing Authentication
---------------------

**Test Session Authentication:**

.. code-block:: python

    from django.test import TestCase
    from django.contrib.auth.models import User
    from django.test import Client
    from rest_framework import status

    class SessionAuthenticationTestCase(TestCase):
        def setUp(self):
            self.client = Client()
            self.user = User.objects.create_user(
                username='testuser',
                password='testpass'
            )

        def test_session_authentication(self):
            # Login through admin
            login_response = self.client.post('/admin/login/', {
                'username': 'testuser',
                'password': 'testpass'
            })
            self.assertEqual(login_response.status_code, 200)
            
            # Access API with session
            response = self.client.get('/api/cms/pages/')
            self.assertEqual(response.status_code, status.HTTP_200_OK) 