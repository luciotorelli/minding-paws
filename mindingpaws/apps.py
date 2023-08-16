from django.apps import AppConfig


class MindingpawsConfig(AppConfig):
    """
    Configuration class for the Mindingpaws app.

    This configuration class specifies the
        default auto field and the name of the app.

    Attributes:
        default_auto_field (str): The default auto field setting for the app.
        name (str): The name of the app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mindingpaws'
