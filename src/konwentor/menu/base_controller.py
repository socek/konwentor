from konwentor.auth.base_controller import AuthController
from konwentor.flashmsg.helpers import FlashMessageWidget
from konwentor.flashmsg.models import FlashMessage

from .helpers import MenuWidget


class MenuController(AuthController):

    menu_highlighted = None

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('menu', MenuWidget, self.menu_highlighted)
        self.add_helper('flashmsg', FlashMessageWidget)

    def add_flashmsg(self, *args, **kwargs):
        data = self.session.get('flash_messages', [])
        data.append(FlashMessage(*args, **kwargs).to_dict())
        self.session['flash_messages'] = data
