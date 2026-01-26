from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    name = 'my_apps.usuarios'

    def ready(self):
        import my_apps.usuarios.signals 