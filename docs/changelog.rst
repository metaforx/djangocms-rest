Changelog
=========

All notable changes to djangocms-rest will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

**Added:**
* Initial documentation structure with Sphinx
* Comprehensive API documentation
* Installation and configuration guides
* Authentication and permissions documentation
* Caching guide with examples
* Contributing guidelines

**Changed:**
* Updated project dependencies to include Sphinx documentation tools

[0.1.0] - 2024-01-01
--------------------

**Added:**
* Initial release of djangocms-rest
* Pages API with full CRUD operations
* Placeholders API for managing page content areas
* Plugins API for managing CMS plugins
* Languages API for multi-language support
* Authentication support (Session, Token, JWT, OAuth2)
* Permission system based on Django CMS permissions
* Caching support with configurable backends
* Pagination and filtering support
* Comprehensive test suite
* Basic documentation

**Features:**
* Complete page management (create, read, update, delete)
* Page tree structure support
* Multi-language content management
* Placeholder and plugin management
* Flexible authentication options
* Role-based permissions
* Performance optimization with caching
* RESTful API design following best practices

**Technical:**
* Built with Django REST Framework
* Compatible with Django 4.2+ and django CMS 5.0+
* Python 3.9+ support
* Comprehensive type hints
* Extensive test coverage
* Pre-commit hooks for code quality

**Documentation:**
* Basic README with installation instructions
* API endpoint documentation
* Configuration examples
* Authentication setup guide

**Testing:**
* Unit tests for all API endpoints
* Integration tests for authentication and permissions
* Test coverage for serializers and views
* Tox configuration for multiple Django/django CMS versions

**Dependencies:**
* Django >= 4.2
* django CMS >= 5.0
* Django REST Framework >= 3.14
* djangocms-link >= 5.0.0
* djangocms-text >= 0.8.0

**Development:**
* Poetry for dependency management
* Pre-commit hooks for code quality
* Type checking with mypy
* Code formatting with Black
* Import sorting with isort
* Linting with flake8

**Contributors:**
* Fabian Braun (@fsbraun) - Initial development
* Django CMS Association - Project support

**Known Issues:**
* Limited plugin type support (only text and link plugins included)
* No support for custom page models
* Basic caching implementation
* Limited documentation

**Future Plans:**
* Support for more plugin types
* Custom page model support
* Advanced caching strategies
* Comprehensive documentation
* API versioning support
* Webhook support
* GraphQL support (optional)
* Headless CMS features
* Content synchronization tools
* Performance monitoring
* API rate limiting
* Content validation
* Bulk operations
* Content import/export tools 