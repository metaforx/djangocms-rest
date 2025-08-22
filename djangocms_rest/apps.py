from django.apps import AppConfig


class DjangocmsRestConfig(AppConfig):
    """
    AppConfig for the djangocms_rest application.
    This application provides RESTful APIs for Django CMS.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "djangocms_rest"
    verbose_name = "Django CMS REST API"
