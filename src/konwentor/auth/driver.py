from konwentor.application.driver import KonwentorDriver
from haplugin.auth.driver import AuthDriver
from .models import User, Permission


class UserDriver(KonwentorDriver):
    name = 'User'
    model = User


class PermissionDriver(KonwentorDriver):
    name = 'Permission'
    model = Permission


class KonwentorAuthDriver(AuthDriver, KonwentorDriver):
    pass
