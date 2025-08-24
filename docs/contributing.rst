Contributing
============

Thank you for your interest in contributing to django CMS REST! This guide will help you get started with contributing to the project.

Getting Started
--------------

**Prerequisites:**

* Python 3.9 or higher
* Git
* A GitHub account

**Fork and Clone:**

1. Fork the repository on GitHub
2. Clone your fork locally:

.. code-block:: bash

    git clone https://github.com/your-username/djangocms-rest.git
    cd djangocms-rest

**Set up Development Environment:**

.. code-block:: bash

    # Install Poetry (if not already installed)
    curl -sSL https://install.python-poetry.org | python3 -

    # Install dependencies
    poetry install

    # Install development dependencies
    poetry install --with dev

    # Activate virtual environment
    poetry shell

**Run Tests:**

.. code-block:: bash

    # Run all tests
    pytest

    # Run tests with coverage
    pytest --cov=djangocms_rest

    # Run specific test file
    pytest tests/test_pages.py

Development Guidelines
--------------------

**Code Style:**

* Follow PEP 8 style guidelines
* Use Black for code formatting
* Use isort for import sorting
* Use flake8 for linting

**Pre-commit Hooks:**

The project uses pre-commit hooks to ensure code quality:

.. code-block:: bash

    # Install pre-commit hooks
    pre-commit install

    # Run pre-commit on all files
    pre-commit run --all-files

**Type Hints:**

* Use type hints for all function parameters and return values
* Use mypy for type checking

.. code-block:: bash

    # Run type checking
    mypy djangocms_rest/

**Documentation:**

* Write docstrings for all functions and classes
* Update documentation when adding new features
* Follow the existing documentation style

**Testing:**

* Write tests for all new features
* Ensure all tests pass before submitting a PR
* Aim for high test coverage

Making Changes
-------------

**Create a Feature Branch:**

.. code-block:: bash

    git checkout -b feature/your-feature-name

**Make Your Changes:**

1. Write your code following the guidelines above
2. Add tests for your changes
3. Update documentation if needed
4. Run tests to ensure everything works

**Commit Your Changes:**

Use conventional commits format:

.. code-block:: bash

    # For new features
    git commit -m "feat: add new API endpoint for page templates"

    # For bug fixes
    git commit -m "fix: resolve pagination issue in page list"

    # For documentation
    git commit -m "docs: update installation guide"

    # For tests
    git commit -m "test: add tests for new page creation endpoint"

**Push Your Changes:**

.. code-block:: bash

    git push origin feature/your-feature-name

**Create a Pull Request:**

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template
5. Submit the PR

Pull Request Guidelines
----------------------

**PR Template:**

When creating a pull request, please include:

* **Description:** What does this PR do?
* **Type of change:** Bug fix, feature, documentation, etc.
* **Testing:** How was this tested?
* **Breaking changes:** Are there any breaking changes?
* **Related issues:** Link to any related issues

**Example PR Description:**

.. code-block:: markdown

    ## Description
    
    This PR adds a new API endpoint for retrieving page templates.
    
    ## Type of change
    
    - [ ] Bug fix
    - [x] New feature
    - [ ] Documentation update
    - [ ] Test update
    
    ## Testing
    
    - Added unit tests for the new endpoint
    - Tested manually with curl
    - All existing tests pass
    
    ## Breaking changes
    
    None
    
    ## Related issues
    
    Closes #123

**Review Process:**

1. Automated checks must pass (tests, linting, type checking)
2. At least one maintainer must approve the PR
3. All conversations must be resolved
4. PR must be up to date with the main branch

Issue Guidelines
---------------

**Before Creating an Issue:**

1. Check if the issue has already been reported
2. Search the documentation for solutions
3. Try to reproduce the issue

**Issue Template:**

When creating an issue, please include:

* **Description:** Clear description of the problem
* **Steps to reproduce:** How to reproduce the issue
* **Expected behavior:** What should happen
* **Actual behavior:** What actually happens
* **Environment:** Python version, Django version, etc.
* **Additional context:** Any other relevant information

**Example Issue:**

.. code-block:: markdown

    ## Description
    
    The page creation API endpoint returns a 500 error when creating pages with certain templates.
    
    ## Steps to reproduce
    
    1. Send POST request to `/api/cms/pages/`
    2. Include `template: "custom_template.html"` in the request body
    3. Receive 500 error
    
    ## Expected behavior
    
    Page should be created successfully with the custom template.
    
    ## Actual behavior
    
    Server returns 500 Internal Server Error.
    
    ## Environment
    
    - Python: 3.11
    - Django: 4.2
    - django CMS: 5.0
    - django CMS REST: 0.1.0
    
    ## Additional context
    
    The custom template exists and works in the Django admin.

Development Setup
----------------

**Local Development Server:**

.. code-block:: bash

    # Run the development server
    python manage.py runserver

    # Run with test data
    python manage.py loaddata test_data.json

**Database Setup:**

.. code-block:: bash

    # Create database
    python manage.py migrate

    # Create superuser
    python manage.py createsuperuser

    # Load test data
    python manage.py loaddata test_data.json

**Testing Different Django/Django CMS Versions:**

The project uses tox for testing multiple environments:

.. code-block:: bash

    # Run tests for all environments
    tox

    # Run tests for specific environment
    tox -e py311-dj42-cms50

**Documentation Development:**

.. code-block:: bash

    # Build documentation
    cd docs
    make html

    # Serve documentation locally
    make serve

    # Watch for changes and rebuild
    make watch

Code Organization
----------------

**Project Structure:**

.. code-block:: text

    djangocms_rest/
    ├── djangocms_rest/
    │   ├── __init__.py
    │   ├── permissions.py
    │   ├── serializers/
    │   │   ├── __init__.py
    │   │   ├── pages.py
    │   │   ├── placeholders.py
    │   │   └── plugins.py
    │   ├── utils/
    │   │   ├── __init__.py
    │   │   ├── cache.py
    │   │   └── render.py
    │   ├── urls.py
    │   ├── utils.py
    │   ├── views_base.py
    │   └── views.py
    ├── tests/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── endpoints/
    │   └── test_app/
    ├── docs/
    └── setup.py

**Adding New Features:**

1. **Serializers:** Add new serializers in `djangocms_rest/serializers/`
2. **Views:** Add new views in `djangocms_rest/views.py`
3. **URLs:** Add new URLs in `djangocms_rest/urls.py`
4. **Tests:** Add tests in `tests/endpoints/`
5. **Documentation:** Update relevant documentation files

**Example: Adding a New Endpoint**

.. code-block:: python

    # djangocms_rest/serializers/pages.py
    class PageTemplateSerializer(serializers.Serializer):
        name = serializers.CharField()
        path = serializers.CharField()

    # djangocms_rest/views.py
    class PageTemplateViewSet(viewsets.ReadOnlyModelViewSet):
        serializer_class = PageTemplateSerializer
        
        def get_queryset(self):
            # Return available templates
            return get_cms_templates()

    # djangocms_rest/urls.py
    router.register(r'templates', PageTemplateViewSet, basename='template')

    # tests/endpoints/test_templates.py
    class TestPageTemplates(TestCase):
        def test_list_templates(self):
            response = self.client.get('/api/cms/templates/')
            self.assertEqual(response.status_code, 200)

Release Process
--------------

**Version Management:**

* Follow semantic versioning (MAJOR.MINOR.PATCH)
* Update version in `djangocms_rest/__init__.py`
* Update `CHANGELOG.rst`

**Release Checklist:**

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] Changelog is updated
- [ ] Version is bumped
- [ ] Release notes are written
- [ ] Package is built and tested
- [ ] Release is tagged on GitHub

**Creating a Release:**

.. code-block:: bash

    # Update version
    # Update changelog
    # Create release branch
    git checkout -b release/v1.0.0
    
    # Commit changes
    git commit -m "chore: prepare release v1.0.0"
    
    # Create tag
    git tag v1.0.0
    
    # Push changes
    git push origin release/v1.0.0
    git push origin v1.0.0

Community Guidelines
-------------------

**Code of Conduct:**

* Be respectful and inclusive
* Help others learn and grow
* Provide constructive feedback
* Follow the project's code of conduct

**Communication:**

* Use GitHub issues for bug reports and feature requests
* Use GitHub discussions for questions and general discussion
* Be clear and concise in your communication
* Provide context and examples when asking questions

**Getting Help:**

* Check the documentation first
* Search existing issues and discussions
* Ask questions in GitHub discussions
* Join the community chat (if available)

**Recognition:**

Contributors are recognized in:

* The project's README file
* Release notes
* The project's contributors page

Thank you for contributing to django CMS REST! 