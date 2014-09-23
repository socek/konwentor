from mock import MagicMock
from hatak.plugins.toster.cases import TestCase

from ..helpers import GameEntityWidget


class GameEntityWidgetTests(TestCase):
    prefix_from = GameEntityWidget

    def setUp(self):
        super().setUp()
        self.obj = MagicMock()
        self.widget = self.prefix_from(self.request, self.obj)
        self.add_mock_object(self.widget, 'render_for')

    def test_id(self):
        self.assertEqual(
            self.obj.GameEntity.id,
            self.widget.id)

    def test_name(self):
        self.assertEqual(
            self.obj.name,
            self.widget.name)

    def test_author_name(self):
        self.assertEqual(
            self.obj.author_name,
            self.widget.author_name)

    def test_count(self):
        self.assertEqual(
            self.obj.GameEntity.count,
            self.widget.count)

    def test_active_borrows_len(self):
        self.obj.GameEntity.active_borrows.return_value = [1, 2, 3]
        self.assertEqual(
            3,
            self.widget.active_borrows_len)

    def test_get_list_class_when_in_box(self):
        self.obj.GameEntity.is_in_box = True
        self.assertEqual('warning', self.widget.get_list_class())

    def test_get_list_class_when_not_avalible(self):
        self.obj.GameEntity.is_in_box = False
        self.obj.GameEntity.is_avalible.return_value = False
        self.assertEqual('danger', self.widget.get_list_class())

    def test_get_list_class_when_all_is_avalible(self):
        self.obj.GameEntity.is_in_box = False
        self.obj.GameEntity.is_avalible.return_value = True
        self.obj.GameEntity.active_borrows_len.return_value = 0
        self.assertEqual('success', self.widget.get_list_class())

    def test_get_list_class(self):
        self.obj.GameEntity.is_in_box = False
        self.obj.GameEntity.is_avalible.return_value = True
        self.obj.GameEntity.active_borrows_len.return_value = 1
        self.assertEqual('info', self.widget.get_list_class())

    def test_borrow_when_is_avalible(self):
        self.obj.GameEntity.is_avalible.return_value = True
        self.assertEqual(
            self.mocks['render_for'].return_value,
            self.widget.borrow()
        )
        self.mocks['render_for'].assert_called_once_with(
            'borrow_button.haml',
            {
                'url': self.route.return_value,
            })
        self.route.assert_called_once_with(
            'gameborrow:add',
            obj_id=self.obj.GameEntity.id)

    def test_borrow_when_not_avalible(self):
        self.obj.GameEntity.is_avalible.return_value = False
        self.assertEqual(
            '',
            self.widget.borrow()
        )

    def test_borrow_when_no_access(self):
        self.user.has_access_to_route.return_value = False
        self.obj.GameEntity.is_avalible.return_value = True
        self.assertEqual(
            '',
            self.widget.borrow()
        )

    def test_move_to_box_when_is_not_in_box(self):
        self.obj.GameEntity.is_in_box = False

        self.assertEqual(
            self.mocks['render_for'].return_value,
            self.widget.move_to_box()
        )

        self.mocks['render_for'].assert_called_once_with(
            'move_to_box_button.haml',
            {
                'url': self.route.return_value,
                'game': self.widget,
            })
        self.route.assert_called_once_with(
            'gamecopy:movetobox',
            obj_id=self.obj.GameEntity.id,)

    def test_move_to_box_when_is_in_box(self):
        self.obj.GameEntity.is_in_box = True

        self.assertEqual(
            '',
            self.widget.move_to_box()
        )

    def test_move_to_box_when_no_access(self):
        self.user.has_access_to_route.return_value = False
        self.obj.GameEntity.is_in_box = False
        self.assertEqual(
            '',
            self.widget.move_to_box()
        )

    def test_info(self):
        self.assertEqual(
            self.mocks['render_for'].return_value,
            self.widget.info()
        )
        self.mocks['render_for'].assert_called_once_with(
            'info.haml', {
                'game': self.obj.Game,
            })
