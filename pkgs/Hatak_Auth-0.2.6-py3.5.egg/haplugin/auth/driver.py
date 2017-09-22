from sqlalchemy.orm.exc import NoResultFound

from haplugin.sql.driver import SqlDriver


class AuthDriver(SqlDriver):
    name = 'Auth'

    def __init__(self, user_cls):
        super().__init__()
        self.model = user_cls
        self.permission_model = user_cls._permission_cls

    def get_by_email(self, email):
        return self.query(self.model).filter_by(email=email).first()

    def create(
        self,
        password=None,
        permissions=None,
        **kwargs
    ):
        obj = self.model()
        for key, value in kwargs.items():
            setattr(obj, key, value)

        if password:
            obj.set_password(password)

        permissions = permissions or []
        for perm in permissions:
            self.add_permission(obj, *perm)

        self.db.add(obj)
        return obj

    def add_permission(self, user, group, name):
        permission = self.get_or_create_permission(group, name)
        user.permissions.append(permission)

    def remove_permission(self, user, group, name):
        for permission in user.permissions:
            if permission.group == group and permission.name == name:
                user.permissions.remove(permission)
                return

    def get_or_create_permission(self, group, name):
        try:
            return (
                self.query(self.permission_model)
                .filter_by(group=group, name=name)
                .one()
            )
        except NoResultFound:
            permission = self.permission_model(group=group, name=name)
            self.db.add(permission)
            return permission
