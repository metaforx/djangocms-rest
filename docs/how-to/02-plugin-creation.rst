Plugin Creation & Serialization
================================

DjangoCMS REST provides basic support for all CMS plugins. This means that all plugins are automatically serialized into JSON data, without the need for any additional configuration.

For most simple use cases, this is all you need. However, when used in relation to other models, you might want to create a custom serializer.

.. note::
    This guide assumes you have a running Django CMS project and a basic understanding of Django CMS plugins. If you are not familiar with them, please refer to the `Django CMS documentation <https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html>`_.

Automatic Serialization
-----------------------

You can use the ``GenericPluginSerializer`` whenever no further application relationship is required. No additional configuration is required — simply create Django CMS plugins according to the documentation.

**Requirements:**

- No model fields needed
- Fields are directly available as model fields
- Fields are standard Django model fields

**Limitations:**

- Foreign keys are automatically resolved but not serialized.


Use Cases
~~~~~~~~~

- Layout plugins like Grid, Row, Column, etc.
- Content plugins like Text, Image, Video, etc.
- Content-Group plugins like Hero, CTAs, etc.

You can also nest plugins inside other plugins as you would normally do in Django CMS.

Example
~~~~~~~

Create your plugin as you would normally do in Django CMS.

Even though we finally will render the plugin decoupled in the frontend, likely using json data in combination with a frontend framework (Vue.js, React, etc.). 
We still define a template for the plugin. This allows us to display the plugin in the django CMS backend for editing purposes and also to pass rendered HTML to the frontend.

Place your plugins in ``cms_plugins.py.`` For our example, include the following code:

.. code-block:: python

    # A simple example of a plugin that renders a static template.
    # No additional configuration is required for serialization.

    from cms.plugin_base import CMSPluginBase
    from cms.plugin_pool import plugin_pool
    from cms.models.pluginmodel import CMSPlugin
    from django.utils.translation import gettext_lazy as _

    @plugin_pool.register_plugin
    class HelloPlugin(CMSPluginBase):
        model = CMSPlugin
        render_template = "hello_world.html" # Adjust the path to your template.
..

Add the following into the root template directory in a file called ``hello_world.html``:

.. code-block:: html+django

    <h1>Hello World!</h1>
    <p>This is a simple example of a plugin that renders a static template.</p>
.. 

Now add this plugin to a placeholder in a page. 

Depending on your projects configuration, you might have to configure placeholders in the ``CMS_PLACEHOLDER_CONF`` setting. See the `Django CMS documentation <https://docs.django-cms.org/en/latest/reference/configuration.html#cms-placeholders>`_ for more information.

After adding the plugin to a placeholder, you can retrieve the content of the placeholder using the :doc:`Pages <../reference/pages>` and :doc:`Placeholders <../reference/placeholders>` endpoints.

.. note::
    We first have to retrieve the page object and then the associated placeholder objects. This is necessary because django CMS placeholders are linked to the page object, not part of the page object. This allows to use preview mode and versioning.


.. code-block:: bash

    # Get page details for a specific page
    #replace language code and the path with your page path.
    curl -X GET "http://localhost:8080/api/en/pages/my-page-with-hello-world-plugin/" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
..

**Response from the pages endpoint:**

.. code-block:: json

    "...",
    "placeholders": [
    {
        "content_type_id": 5,
        "object_id": 9,
        "slot": "content",
        "details": "http://localhost:8080/api/en/placeholders/5/9/content/"
    }
    ],
    "...",
..

.. code-block:: bash

    # Get placeholder content for a specific placeholder
    # replace query with parameters from the response of the pages endpoint.
    curl -X GET "http://localhost:8080/api/en/placeholders/5/9/content/?html=1" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
..

.. note::
    ?html=1 will render the plugin as HTML.


**Response from the placeholders endpoint:**

.. code-block:: json

    {
        "slot": "content",
        "label": "Content",
        "language": "en",
        "content": [
            {
                "plugin_type": "HelloPlugin"
            }
        ],
        "html": "<h1>Hello World!</h1>\n<p>This is a simple example of a plugin that renders a static template.</p>"
    }

..

As you can see, the content is serialized as a list of plugins. Each plugin has a ``plugin_type`` that helps identify and render the plugin correctly on the frontend.

In the above example, we would simply render the HTML in the frontend.

You can retrieve all plugin details using the :doc:`Plugins <../reference/plugins>` endpoint.

.. hint::
    You can setup a vue.js frontend application to handle the rendering of json data. Follow the guide `Setup Vue.js Project <01-use-multi-site.html#setup-vue-js-project>`_ to get started.



Custom Serialization
---------------------

...coming soon...

