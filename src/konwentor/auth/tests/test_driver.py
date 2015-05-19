from ..driver import KonwentorAuthDriver
from ..models import User

from haplugin.sql.testing import DatabaseFixture


class TestKonwentorAuthDriver(DatabaseFixture):

    def test_removing_permissions(self, db, driver, fixtures):
        def permissions(user):
            permissions = set()
            for permission in user.permissions:
                permissions.add((permission.group, permission.name))
            return permissions

        driver.add_group(KonwentorAuthDriver(User))
        user = fixtures['User']['first']

        try:
            driver.Auth.remove_permission(user, 'gamecopy', 'add')
            db.flush()

            assert permissions(user) == set([
                ('base', 'view'),
                ('game', 'add'),
                ('game', 'edit'),
                ('convent', 'add'),
                ('gameborrow', 'add'),
            ])
        finally:
            driver.Auth.add_permission(user, 'gamecopy', 'add')
            db.flush()
