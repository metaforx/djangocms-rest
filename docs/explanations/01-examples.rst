Examples
========

This section provides practical examples of using djangocms-rest in various scenarios.

Basic Examples
-------------

**Creating a Page with Content:**

.. code-block:: python

    import requests

    # API configuration
    API_BASE_URL = 'http://localhost:8000/api/cms'
    HEADERS = {
        'Authorization': 'Token your-token-here',
        'Content-Type': 'application/json'
    }

    # Create a new page
    page_data = {
        'title': 'Welcome to Our Site',
        'slug': 'welcome',
        'language': 'en',
        'template': 'page.html',
        'is_published': True,
        'meta_description': 'Welcome to our website'
    }

    response = requests.post(
        f'{API_BASE_URL}/pages/',
        json=page_data,
        headers=HEADERS
    )

    if response.status_code == 201:
        page = response.json()
        print(f"Created page: {page['title']} (ID: {page['id']})")
        
        # Add content to the page
        placeholder_data = {
            'slot': 'content',
            'page': page['id']
        }
        
        placeholder_response = requests.post(
            f'{API_BASE_URL}/placeholders/',
            json=placeholder_data,
            headers=HEADERS
        )
        
        if placeholder_response.status_code == 201:
            placeholder = placeholder_response.json()
            
            # Add a text plugin
            plugin_data = {
                'plugin_type': 'TextPlugin',
                'body': '<p>Welcome to our website! This is the main content.</p>'
            }
            
            plugin_response = requests.post(
                f'{API_BASE_URL}/placeholders/{placeholder["id"]}/plugins/',
                json=plugin_data,
                headers=HEADERS
            )
            
            if plugin_response.status_code == 201:
                print("Content added successfully!")

**Building a Page Tree:**

.. code-block:: python

    def build_page_tree():
        """Create a hierarchical page structure"""
        
        # Create home page
        home_data = {
            'title': 'Home',
            'slug': 'home',
            'language': 'en',
            'template': 'page.html',
            'is_published': True
        }
        
        home_response = requests.post(
            f'{API_BASE_URL}/pages/',
            json=home_data,
            headers=HEADERS
        )
        home_page = home_response.json()
        
        # Create about page under home
        about_data = {
            'title': 'About Us',
            'slug': 'about',
            'language': 'en',
            'template': 'page.html',
            'is_published': True,
            'parent': home_page['id']
        }
        
        about_response = requests.post(
            f'{API_BASE_URL}/pages/',
            json=about_data,
            headers=HEADERS
        )
        about_page = about_response.json()
        
        # Create contact page under home
        contact_data = {
            'title': 'Contact',
            'slug': 'contact',
            'language': 'en',
            'template': 'page.html',
            'is_published': True,
            'parent': home_page['id']
        }
        
        contact_response = requests.post(
            f'{API_BASE_URL}/pages/',
            json=contact_data,
            headers=HEADERS
        )
        
        print("Page tree created successfully!")

Advanced Examples
----------------

**Multi-language Content Management:**

.. code-block:: python

    def create_multilingual_content():
        """Create content in multiple languages"""
        
        # English content
        en_page_data = {
            'title': 'Welcome',
            'slug': 'welcome',
            'language': 'en',
            'template': 'page.html',
            'is_published': True
        }
        
        en_response = requests.post(
            f'{API_BASE_URL}/pages/',
            json=en_page_data,
            headers=HEADERS
        )
        en_page = en_response.json()
        
        # German content (translation)
        de_page_data = {
            'title': 'Willkommen',
            'slug': 'willkommen',
            'language': 'de',
            'template': 'page.html',
            'is_published': True
        }
        
        de_response = requests.post(
            f'{API_BASE_URL}/pages/',
            json=de_page_data,
            headers=HEADERS
        )
        de_page = de_response.json()
        
        # Add content to both pages
        for page in [en_page, de_page]:
            content = "Welcome to our site!" if page['language'] == 'en' else "Willkommen auf unserer Seite!"
            
            # Add placeholder and content
            placeholder_data = {'slot': 'content', 'page': page['id']}
            placeholder_response = requests.post(
                f'{API_BASE_URL}/placeholders/',
                json=placeholder_data,
                headers=HEADERS
            )
            
            if placeholder_response.status_code == 201:
                placeholder = placeholder_response.json()
                
                plugin_data = {
                    'plugin_type': 'TextPlugin',
                    'body': f'<p>{content}</p>'
                }
                
                requests.post(
                    f'{API_BASE_URL}/placeholders/{placeholder["id"]}/plugins/',
                    json=plugin_data,
                    headers=HEADERS
                )

**Bulk Content Import:**

.. code-block:: python

    import json
    from typing import List, Dict

    def import_content_from_json(file_path: str):
        """Import content from a JSON file"""
        
        with open(file_path, 'r') as f:
            content_data = json.load(f)
        
        created_pages = []
        
        for page_data in content_data['pages']:
            # Create page
            response = requests.post(
                f'{API_BASE_URL}/pages/',
                json=page_data,
                headers=HEADERS
            )
            
            if response.status_code == 201:
                page = response.json()
                created_pages.append(page)
                
                # Add placeholders and plugins
                if 'placeholders' in page_data:
                    for placeholder_data in page_data['placeholders']:
                        placeholder_data['page'] = page['id']
                        
                        placeholder_response = requests.post(
                            f'{API_BASE_URL}/placeholders/',
                            json=placeholder_data,
                            headers=HEADERS
                        )
                        
                        if placeholder_response.status_code == 201:
                            placeholder = placeholder_response.json()
                            
                            # Add plugins
                            if 'plugins' in placeholder_data:
                                for plugin_data in placeholder_data['plugins']:
                                    requests.post(
                                        f'{API_BASE_URL}/placeholders/{placeholder["id"]}/plugins/',
                                        json=plugin_data,
                                        headers=HEADERS
                                    )
        
        return created_pages

**Content Synchronization:**

.. code-block:: python

    def sync_content_between_environments(source_url: str, target_url: str):
        """Sync content between development and production environments"""
        
        # Get all pages from source
        source_response = requests.get(
            f'{source_url}/api/cms/pages/',
            headers=HEADERS
        )
        source_pages = source_response.json()
        
        # Get all pages from target
        target_response = requests.get(
            f'{target_url}/api/cms/pages/',
            headers=HEADERS
        )
        target_pages = target_response.json()
        
        # Find pages that need to be created or updated
        source_page_dict = {page['slug']: page for page in source_pages['results']}
        target_page_dict = {page['slug']: page for page in target_pages['results']}
        
        for slug, source_page in source_page_dict.items():
            if slug not in target_page_dict:
                # Create new page
                create_data = {k: v for k, v in source_page.items() 
                             if k not in ['id', 'created_date', 'changed_date']}
                
                requests.post(
                    f'{target_url}/api/cms/pages/',
                    json=create_data,
                    headers=HEADERS
                )
                print(f"Created page: {slug}")
            
            elif source_page['changed_date'] > target_page_dict[slug]['changed_date']:
                # Update existing page
                update_data = {k: v for k, v in source_page.items() 
                             if k not in ['id', 'created_date', 'changed_date']}
                
                requests.put(
                    f'{target_url}/api/cms/pages/{target_page_dict[slug]["id"]}/',
                    json=update_data,
                    headers=HEADERS
                )
                print(f"Updated page: {slug}")

Client Libraries
---------------

**Python Client Library:**

.. code-block:: python

    class DjangoCMSRESTClient:
        """A client library for djangocms-rest API"""
        
        def __init__(self, base_url: str, token: str = None, username: str = None, password: str = None):
            self.base_url = base_url.rstrip('/')
            self.session = requests.Session()
            
            if token:
                self.session.headers.update({
                    'Authorization': f'Token {token}',
                    'Content-Type': 'application/json'
                })
            elif username and password:
                self.session.auth = (username, password)
        
        def get_pages(self, **params):
            """Get pages with optional filtering"""
            response = self.session.get(f'{self.base_url}/api/cms/pages/', params=params)
            response.raise_for_status()
            return response.json()
        
        def get_page(self, page_id: int):
            """Get a specific page by ID"""
            response = self.session.get(f'{self.base_url}/api/cms/pages/{page_id}/')
            response.raise_for_status()
            return response.json()
        
        def create_page(self, page_data: dict):
            """Create a new page"""
            response = self.session.post(f'{self.base_url}/api/cms/pages/', json=page_data)
            response.raise_for_status()
            return response.json()
        
        def update_page(self, page_id: int, page_data: dict):
            """Update an existing page"""
            response = self.session.put(f'{self.base_url}/api/cms/pages/{page_id}/', json=page_data)
            response.raise_for_status()
            return response.json()
        
        def delete_page(self, page_id: int):
            """Delete a page"""
            response = self.session.delete(f'{self.base_url}/api/cms/pages/{page_id}/')
            response.raise_for_status()
        
        def get_placeholders(self, page_id: int):
            """Get placeholders for a page"""
            response = self.session.get(f'{self.base_url}/api/cms/pages/{page_id}/placeholders/')
            response.raise_for_status()
            return response.json()
        
        def add_plugin(self, placeholder_id: int, plugin_data: dict):
            """Add a plugin to a placeholder"""
            response = self.session.post(
                f'{self.base_url}/api/cms/placeholders/{placeholder_id}/plugins/',
                json=plugin_data
            )
            response.raise_for_status()
            return response.json()

    # Usage
    client = DjangoCMSRESTClient(
        'http://localhost:8000',
        token='your-token-here'
    )
    
    # Get all published pages
    pages = client.get_pages(is_published=True, language='en')
    
    # Create a new page
    new_page = client.create_page({
        'title': 'New Page',
        'slug': 'new-page',
        'language': 'en',
        'template': 'page.html',
        'is_published': True
    })

**JavaScript Client Library:**

.. code-block:: javascript

    class DjangoCMSRESTClient {
        constructor(baseUrl, token = null, username = null, password = null) {
            this.baseUrl = baseUrl.replace(/\/$/, '');
            this.token = token;
            this.username = username;
            this.password = password;
        }
        
        async request(endpoint, options = {}) {
            const url = `${this.baseUrl}${endpoint}`;
            const headers = {
                'Content-Type': 'application/json',
                ...options.headers
            };
            
            if (this.token) {
                headers['Authorization'] = `Token ${this.token}`;
            }
            
            const config = {
                ...options,
                headers
            };
            
            if (this.username && this.password) {
                config.auth = `${this.username}:${this.password}`;
            }
            
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return response.json();
        }
        
        async getPages(params = {}) {
            const queryString = new URLSearchParams(params).toString();
            const endpoint = `/api/cms/pages/${queryString ? '?' + queryString : ''}`;
            return this.request(endpoint);
        }
        
        async getPage(pageId) {
            return this.request(`/api/cms/pages/${pageId}/`);
        }
        
        async createPage(pageData) {
            return this.request('/api/cms/pages/', {
                method: 'POST',
                body: JSON.stringify(pageData)
            });
        }
        
        async updatePage(pageId, pageData) {
            return this.request(`/api/cms/pages/${pageId}/`, {
                method: 'PUT',
                body: JSON.stringify(pageData)
            });
        }
        
        async deletePage(pageId) {
            return this.request(`/api/cms/pages/${pageId}/`, {
                method: 'DELETE'
            });
        }
        
        async getPlaceholders(pageId) {
            return this.request(`/api/cms/pages/${pageId}/placeholders/`);
        }
        
        async addPlugin(placeholderId, pluginData) {
            return this.request(`/api/cms/placeholders/${placeholderId}/plugins/`, {
                method: 'POST',
                body: JSON.stringify(pluginData)
            });
        }
    }

    // Usage
    const client = new DjangoCMSRESTClient('http://localhost:8000', 'your-token-here');
    
    // Get all pages
    client.getPages({ is_published: true, language: 'en' })
        .then(pages => console.log('Pages:', pages))
        .catch(error => console.error('Error:', error));
    
    // Create a new page
    client.createPage({
        title: 'New Page',
        slug: 'new-page',
        language: 'en',
        template: 'page.html',
        is_published: true
    })
        .then(page => console.log('Created page:', page))
        .catch(error => console.error('Error:', error));

Integration Examples
-------------------

**Django Management Command:**

.. code-block:: python

    # management/commands/import_content.py
    from django.core.management.base import BaseCommand
    from djangocms_rest.client import DjangoCMSRESTClient

    class Command(BaseCommand):
        help = 'Import content from external source'

        def add_arguments(self, parser):
            parser.add_argument('source_url', type=str)
            parser.add_argument('--token', type=str)

        def handle(self, *args, **options):
            client = DjangoCMSRESTClient(
                'http://localhost:8000',
                token=options['token']
            )
            
            # Import content logic here
            self.stdout.write('Content import completed!')

**Celery Task:**

.. code-block:: python

    from celery import shared_task
    from djangocms_rest.client import DjangoCMSRESTClient

    @shared_task
    def sync_content_task():
        """Background task to sync content"""
        client = DjangoCMSRESTClient(
            'http://localhost:8000',
            token='your-token-here'
        )
        
        # Sync logic here
        return "Content sync completed"

**Django Signal Handler:**

.. code-block:: python

    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from cms.models import Page
    from djangocms_rest.client import DjangoCMSRESTClient

    @receiver(post_save, sender=Page)
    def sync_page_to_external_system(sender, instance, created, **kwargs):
        """Sync page changes to external system"""
        client = DjangoCMSRESTClient(
            'https://external-api.com',
            token='external-token'
        )
        
        if created:
            client.create_page({
                'title': instance.title,
                'slug': instance.get_slug(),
                'language': instance.language,
                'is_published': instance.is_published
            })
        else:
            client.update_page(instance.id, {
                'title': instance.title,
                'slug': instance.get_slug(),
                'language': instance.language,
                'is_published': instance.is_published
            })

**Webhook Integration:**

.. code-block:: python

    from django.http import HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    from django.views.decorators.http import require_http_methods
    import json
    from djangocms_rest.client import DjangoCMSRESTClient

    @csrf_exempt
    @require_http_methods(["POST"])
    def webhook_handler(request):
        """Handle webhooks from external systems"""
        data = json.loads(request.body)
        
        client = DjangoCMSRESTClient(
            'http://localhost:8000',
            token='your-token-here'
        )
        
        if data['event'] == 'page_created':
            # Handle page creation
            pass
        elif data['event'] == 'page_updated':
            # Handle page update
            pass
        
        return HttpResponse(status=200) 