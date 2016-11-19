from mock import MagicMock, patch
from pytest import fixture, yield_fixture

from hatak.testing import RequestFixture

from ..helpers import GameEntityWidget


class TestGameEntityWidget(RequestFixture):

    @fixture
    def obj(self):
        return MagicMock()

    @fixture
    def widget(self, request, obj):
        return GameEntityWidget(request, obj)

    @yield_fixture
    def render_for(self, widget):
        with patch.object(widget, 'render_for') as mock:
            yield mock

    @fixture
    def route(self, request):
        return request.route_path

    def test_id(self, widget, obj):
        assert widget.id == obj.GameEntity.id

    def test_name(self, widget, obj):
        assert widget.name == obj.name

    def test_author_name(self, widget, obj):
        assert widget.author_name == obj.author_name

    def test_count(self, widget, obj):
        assert widget.count == obj.GameEntity.count

    def test_active_borrows_len(self, widget, obj):
        obj.GameEntity.active_borrows.return_value = [1, 2, 3]
        assert widget.active_borrows_len == 3

    def test_get_list_class_when_in_box(self, widget, obj):
        obj.GameEntity.is_in_box = True
        assert widget.get_list_class() == 'warning'

    def test_get_list_class_when_not_avalible(self, widget, obj):
        obj.GameEntity.is_in_box = False
        obj.GameEntity.is_avalible.return_value = False
        assert widget.get_list_class() == 'danger'

    def test_get_list_class_when_all_is_avalible(self, widget, obj):
        obj.GameEntity.is_in_box = False
        obj.GameEntity.is_avalible.return_value = True
        obj.GameEntity.active_borrows_len.return_value = 0
        assert widget.get_list_class() == 'success'

    def test_get_list_class(self, widget, obj):
        obj.GameEntity.is_in_box = False
        obj.GameEntity.is_avalible.return_value = True
        obj.GameEntity.active_borrows_len.return_value = 1
        assert widget.get_list_class() == 'info'

    def test_borrow_when_is_avalible(
        self,
        widget,
        obj,
        render_for,
        route,
        matchdict
    ):
        matchdict['room_id'] = '12345'
        matchdict['convent_id'] = '123'

        obj.GameEntity.is_avalible.return_value = True
        assert widget.borrow(), render_for.return_value

        render_for.assert_called_once_with(
            'borrow_button.haml',
            {
                'url': route.return_value,
            })
        route.assert_called_once_with(
            'gameborrow:add',
            obj_id=obj.GameEntity.id,
            room_id=matchdict['room_id'],
            convent_id=matchdict['convent_id'],
        )

    def test_borrow_when_not_avalible(self, widget, obj):
        obj.GameEntity.is_avalible.return_value = False
        assert widget.borrow() == ''

    def test_borrow_when_no_access(self, widget, obj):
        self.user.has_access_to_route.return_value = False
        obj.GameEntity.is_avalible.return_value = True
        assert widget.borrow() == ''

    def test_move_to_box_when_is_not_in_box(
        self,
        widget,
        obj,
        render_for,
        route,
        matchdict
    ):
        matchdict['room_id'] = '1234'
        matchdict['convent_id'] = '12'
        obj.GameEntity.is_in_box = False

        assert widget.move_to_box() == render_for.return_value

        render_for.assert_called_once_with(
            'move_to_box_button.haml',
            {
                'url': route.return_value,
                'game': widget,
            })
        route.assert_called_once_with(
            'gamecopy:movetobox',
            obj_id=obj.GameEntity.id,
            room_id=matchdict['room_id'],
            convent_id=matchdict['convent_id'],
        )

    def test_move_to_box_when_is_in_box(self, widget, obj):
        obj.GameEntity.is_in_box = True

        assert widget.move_to_box() == ''

    def test_move_to_box_when_no_access(self, widget, obj):
        self.user.has_access_to_route.return_value = False
        obj.GameEntity.is_in_box = False
        assert widget.move_to_box() == ''

    def testinfo(self, widget, obj, render_for):
        assert widget.info() == render_for.return_value
        render_for.assert_called_once_with(
            'info.haml', {
                'game': obj.Game,
            })
