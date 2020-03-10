from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    #import hàm tạo profile khi tạo tài khoản vào app.py
    def ready(self):
        import users.signals