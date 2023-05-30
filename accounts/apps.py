from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # IMPORTS SIGNAL WHEN APPS READY
    def ready(self):
        import accounts.signals
