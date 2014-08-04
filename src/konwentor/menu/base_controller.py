from konwentor.auth.base_controller import AuthController

from .helpers import MenuWidget


class MenuController(AuthController):

    menu_highlighted = None

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('menu', MenuWidget, self.menu_highlighted)
