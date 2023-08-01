from django.apps import AppConfig


class PollvoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pollvote'
    
    def ready(self):
        import pollvote.signals
