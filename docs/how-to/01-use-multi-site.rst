Use Multi-Site in your frontend
===============================

In this short guide, we will show you how to use the multi-site functionality in your frontend app.
As you are reading this we assume you have a basic understanding of decoupled architecture and frontend frameworks. There are plenty of articles and guides on the internet to get you started, like:

- `Decoupled Architecture Microservices <https://medium.com/@saurabh.engg.it/decoupled-architecture-microservices-29f7b201bd87>`_

We will use ``vue.js`` to show how to fetch data from different sites. This implemenation
guide can easily be adapted to other frontend frameworks.

.. note::
    This guide assumes you have a running Django CMS project with multiple sites.
    If you haven't set up multi-site yet, please follow the :doc:`../tutorial/01-installation` guide...

.. hint::
    Setup a basic vue.js project using `Vue.js Quick Start <https://vuejs.org/guide/quick-start>`_

CMS Reference
-------------
- `Django CMS User Docs - Pages <https://user-guide.django-cms.org/en/latest/tutorial/05-pagetree.html>`_

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


Response
--------

You should get a response described in the :doc:`../reference/pages` documentation.


Vue.js Sample
-------------

Before using this example, you should set up a basic Vue.js project.
If you are familiar with JavaScript frameworks, you can get started right away.

- `Vue.js Quick Start <https://vuejs.org/guide/quick-start>`_


Simple Vue.js example to fetch page tree with X-Site-ID header:

.. code-block:: vue

    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    </head>
    <body>
        <div id="app">
            <select v-model="siteId" @change="fetchData">
                <option value="1">Site 1</option>
                <option value="2">Site 2</option>
            </select>
            <button @click="fetchData">Fetch Page Tree</button>
            <pre>{{ data }}</pre>
        </div>

        <script>
            const { createApp } = Vue;
            createApp({
                data() {
                    return {
                        siteId: '1',
                        data: null
                    }
                },
                methods: {
                    async fetchData() {
                        const response = await fetch('http://localhost:8080/api/cms/en/pages-tree/', {
                            headers: { 'X-Site-ID': this.siteId }
                        });
                        this.data = await response.json();
                    }
                }
            }).mount('#app');
        </script>
    </body>
    </html>