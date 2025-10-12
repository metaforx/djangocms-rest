Use Multi-Site with your frontend app
=====================================

In this short guide, we will show you how to use the multi-site functionality in your frontend app.
We will use ``vue.js`` to show how to fetch data from different sites. This implemenation
guide can easily be adapted to other frontend frameworks.

.. note::
    This guide assumes you have a running Django CMS project with multiple sites.
    If you haven't set up multi-site yet, please follow the :doc:`../tutorial/01-installation` guide.

CMS Reference
-------------
- `Django CMS - Pages <https://user-guide.django-cms.org/en/latest/tutorial/05-pagetree.html>`_

Example
-------

1. Adjust the primary site details for site A (Site ID 1)
2. Create a new site for site B (Site ID 2)
3. Create a page tree for site A
4. Create a page tree for site B
5. Fetch the page tree for site A.
6. Fetch the page tree for site B.


.. code-block:: bash

    # Fetch the page tree for site A
    curl -H "X-Site-ID: 1" \
        -H "Content-Type: application/json" \
        http://localhost:8080/api/cms/en/pages-tree/


Sample Response
---------------

You should get a response described in the :doc:`../reference/pages` documentation.