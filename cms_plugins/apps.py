from django.apps import AppConfig


class CmsPluginsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"  # type: ignore
    name = "cms_plugins"
    
    def ready(self):
        import cms_plugins.signals