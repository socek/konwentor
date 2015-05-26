class ListAvaliblePermissions(object):

    def __init__(self, request, user=None):
        self.request = request
        self.route = request.registry['route']
        self.user = user

    def get_all(self):
        self.gather_user_permissions()
        self.avalible_permissions = set()
        for permission in self.get_all_permissions():
            yield permission
            self.avalible_permissions.add(permission)

    def gather_user_permissions(self):
        self.user_permissions = set()
        if self.user:
            for permission in self.user.permissions:
                self.user_permissions.add(permission.to_str())

    def get_all_permissions(self):
        for route in self.route.routes.values():
            try:
                for permission in route.permissions:
                    permission_str = '%s:%s' % permission
                    if self.is_permission_avalible(permission_str):
                        yield permission_str
            except AttributeError:
                pass

    def is_permission_avalible(self, permission):
        return (
            permission not in self.avalible_permissions
            and permission not in self.user_permissions
        )
