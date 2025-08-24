Permissions
===========

django CMS REST uses Django's permission system to control access to API endpoints. This guide explains how permissions work and how to customize them.

Overview
--------

Permissions in django CMS REST are based on Django's built-in permission system. Each API endpoint checks for specific permissions before allowing access.

Default Permissions
------------------

The following permissions are required by default:

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

Permission Classes
-----------------

django CMS REST provides custom permission classes that extend Django REST Framework's permission system:

.. code-block:: python

    from djangocms_rest.permissions import (
        CMSPagePermission,
        CMSPlaceholderPermission,
        CMSPluginPermission,
    )

**CMSPagePermission:**

.. code-block:: python

    class CMSPagePermission(BasePermission):
        """
        Permission class for CMS pages.
        Checks Django CMS permissions for page operations.
        """
        
        def has_permission(self, request, view):
            # Check if user has required permissions
            if view.action == 'create':
                return request.user.has_perm('cms.add_page')
            elif view.action in ['update', 'partial_update']:
                return request.user.has_perm('cms.change_page')
            elif view.action == 'destroy':
                return request.user.has_perm('cms.delete_page')
            elif view.action in ['list', 'retrieve']:
                return request.user.has_perm('cms.view_page')
            return False

        def has_object_permission(self, request, view, obj):
            # Check object-level permissions
            if view.action in ['update', 'partial_update']:
                return request.user.has_perm('cms.change_page')
            elif view.action == 'destroy':
                return request.user.has_perm('cms.delete_page')
            elif view.action == 'retrieve':
                return request.user.has_perm('cms.view_page')
            return False

Customizing Permissions
----------------------

**Custom Permission Class:**

.. code-block:: python

    from rest_framework.permissions import BasePermission
    from djangocms_rest.permissions import CMSPagePermission

    class CustomPagePermission(CMSPagePermission):
        def has_permission(self, request, view):
            # Allow superusers to do anything
            if request.user.is_superuser:
                return True
            
            # Allow staff users to view pages
            if view.action in ['list', 'retrieve'] and request.user.is_staff:
                return True
            
            # Use parent permission logic for other cases
            return super().has_permission(request, view)

        def has_object_permission(self, request, view, obj):
            # Allow page owners to edit their pages
            if hasattr(obj, 'owner') and obj.owner == request.user:
                return True
            
            # Use parent permission logic for other cases
            return super().has_object_permission(request, view, obj)

**Apply Custom Permissions:**

.. code-block:: python

    from djangocms_rest.views import PageViewSet

    class CustomPageViewSet(PageViewSet):
        permission_classes = [CustomPagePermission]

**URL Configuration:**

.. code-block:: python

    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from .views import CustomPageViewSet

    router = DefaultRouter()
    router.register(r'pages', CustomPageViewSet, basename='page')

    urlpatterns = [
        path('api/cms/', include(router.urls)),
    ]

Role-Based Permissions
---------------------

You can implement role-based permissions using Django groups:

.. code-block:: python

    from rest_framework.permissions import BasePermission

    class RoleBasedPermission(BasePermission):
        def has_permission(self, request, view):
            # Check if user is in required group
            if view.action == 'create':
                return request.user.groups.filter(name='Content Editors').exists()
            elif view.action in ['update', 'partial_update']:
                return request.user.groups.filter(name='Content Editors').exists()
            elif view.action == 'destroy':
                return request.user.groups.filter(name='Content Managers').exists()
            elif view.action in ['list', 'retrieve']:
                return True  # Allow read access to all authenticated users
            return False

**Setting up Groups:**

.. code-block:: python

    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from cms.models import Page

    # Create groups
    editors_group, created = Group.objects.get_or_create(name='Content Editors')
    managers_group, created = Group.objects.get_or_create(name='Content Managers')

    # Get CMS permissions
    cms_content_type = ContentType.objects.get_for_model(Page)
    cms_permissions = Permission.objects.filter(content_type=cms_content_type)

    # Assign permissions to groups
    for permission in cms_permissions:
        if 'add' in permission.codename or 'change' in permission.codename:
            editors_group.permissions.add(permission)
        if 'delete' in permission.codename:
            managers_group.permissions.add(permission)

**Assign Users to Groups:**

.. code-block:: python

    from django.contrib.auth.models import User, Group

    # Assign user to group
    user = User.objects.get(username='editor')
    editors_group = Group.objects.get(name='Content Editors')
    user.groups.add(editors_group)

Object-Level Permissions
-----------------------

For more granular control, you can implement object-level permissions:

.. code-block:: python

    from rest_framework.permissions import BasePermission

    class ObjectLevelPermission(BasePermission):
        def has_object_permission(self, request, view, obj):
            # Check if user owns the page
            if hasattr(obj, 'created_by') and obj.created_by == request.user:
                return True
            
            # Check if user is in the page's allowed editors
            if hasattr(obj, 'allowed_editors') and request.user in obj.allowed_editors.all():
                return True
            
            # Check Django CMS permissions
            if view.action in ['update', 'partial_update']:
                return request.user.has_perm('cms.change_page')
            elif view.action == 'destroy':
                return request.user.has_perm('cms.delete_page')
            
            return False

**Custom Page Model with Ownership:**

.. code-block:: python

    from django.db import models
    from cms.models import Page

    class CustomPage(Page):
        created_by = models.ForeignKey(
            'auth.User',
            on_delete=models.CASCADE,
            related_name='created_pages'
        )
        allowed_editors = models.ManyToManyField(
            'auth.User',
            related_name='editable_pages',
            blank=True
        )

Anonymous Access
---------------

To allow anonymous users to read content, configure your settings:

.. code-block:: python

    # settings.py
    DJANGOCMS_REST = {
        'ALLOW_ANONYMOUS_READ': True,
        'REQUIRE_AUTHENTICATION': False,
    }

**Custom Anonymous Permission:**

.. code-block:: python

    from rest_framework.permissions import BasePermission

    class AnonymousReadPermission(BasePermission):
        def has_permission(self, request, view):
            # Allow anonymous users to read
            if view.action in ['list', 'retrieve']:
                return True
            
            # Require authentication for write operations
            return request.user.is_authenticated

        def has_object_permission(self, request, view, obj):
            # Allow anonymous users to read
            if view.action == 'retrieve':
                return True
            
            # Require authentication for write operations
            return request.user.is_authenticated

API-Level Permissions
--------------------

You can also control permissions at the API level:

.. code-block:: python

    from rest_framework.decorators import api_view, permission_classes
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.response import Response

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def custom_page_endpoint(request):
        # This endpoint requires authentication
        return Response({'message': 'Authenticated access only'})

    @api_view(['GET'])
    def public_page_endpoint(request):
        # This endpoint allows anonymous access
        return Response({'message': 'Public access allowed'})

Testing Permissions
------------------

**Test Permission Classes:**

.. code-block:: python

    from django.test import TestCase
    from django.contrib.auth.models import User, Permission
    from django.contrib.contenttypes.models import ContentType
    from cms.models import Page
    from djangocms_rest.permissions import CMSPagePermission

    class PermissionTestCase(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(
                username='testuser',
                password='testpass'
            )
            self.page = Page.objects.create(
                title='Test Page',
                slug='test-page'
            )
            self.permission = CMSPagePermission()

        def test_user_without_permissions(self):
            request = type('Request', (), {'user': self.user})()
            view = type('View', (), {'action': 'create'})()
            
            self.assertFalse(
                self.permission.has_permission(request, view)
            )

        def test_user_with_permissions(self):
            # Add permission to user
            content_type = ContentType.objects.get_for_model(Page)
            permission = Permission.objects.get(
                content_type=content_type,
                codename='add_page'
            )
            self.user.user_permissions.add(permission)
            
            request = type('Request', (), {'user': self.user})()
            view = type('View', (), {'action': 'create'})()
            
            self.assertTrue(
                self.permission.has_permission(request, view)
            )

**Test API Endpoints:**

.. code-block:: python

    from django.test import TestCase
    from django.contrib.auth.models import User
    from rest_framework.test import APIClient
    from rest_framework import status

    class APIPermissionTestCase(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = User.objects.create_user(
                username='testuser',
                password='testpass'
            )

        def test_authenticated_access(self):
            self.client.force_authenticate(user=self.user)
            response = self.client.get('/api/cms/pages/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_unauthenticated_access(self):
            response = self.client.get('/api/cms/pages/')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

Best Practices
-------------

1. **Principle of Least Privilege:**
   * Only grant the minimum permissions necessary
   * Use role-based permissions for better management

2. **Regular Permission Audits:**
   * Regularly review and update permissions
   * Remove permissions from users who no longer need them

3. **Use Groups:**
   * Organize users into groups for easier permission management
   * Assign permissions to groups rather than individual users

4. **Test Permissions:**
   * Write tests to ensure permissions work correctly
   * Test both positive and negative cases

5. **Document Permissions:**
   * Document what permissions are required for each endpoint
   * Keep permission documentation up to date

6. **Monitor Access:**
   * Log permission failures for security monitoring
   * Set up alerts for suspicious access patterns

Example Configuration
--------------------

**Complete Permission Setup:**

.. code-block:: python

    # settings.py
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    }

    DJANGOCMS_REST = {
        'DEFAULT_PERMISSIONS': [
            'cms.add_page',
            'cms.change_page',
            'cms.delete_page',
            'cms.view_page',
        ],
        'ALLOW_ANONYMOUS_READ': False,
        'REQUIRE_AUTHENTICATION': True,
    }

    # views.py
    from djangocms_rest.views import PageViewSet
    from .permissions import CustomPagePermission

    class CustomPageViewSet(PageViewSet):
        permission_classes = [CustomPagePermission]

    # urls.py
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from .views import CustomPageViewSet

    router = DefaultRouter()
    router.register(r'pages', CustomPageViewSet, basename='page')

    urlpatterns = [
        path('api/cms/', include(router.urls)),
    ] 