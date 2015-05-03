from haplugin.jinja2 import Jinja2HelperMany


from konwentor.convent.helpers import has_access_to_route


class GameEntityWidget(Jinja2HelperMany):
    prefix = 'konwentor.gamecopy:templates/widget'

    def __init__(self, request, obj):
        super().__init__(request)
        self.obj = obj

    @property
    def id(self):
        return self.obj.GameEntity.id

    @property
    def name(self):
        return self.obj.name

    @property
    def author_name(self):
        return self.obj.author_name

    @property
    def count(self):
        return self.obj.GameEntity.count

    @property
    def active_borrows_len(self):
        return len(list(self.obj.GameEntity.active_borrows()))

    @has_access_to_route('gameborrow:add')
    def borrow(self):
        if self.obj.GameEntity.is_avalible():
            return self.render_for('borrow_button.haml', {
                'url': self.route(
                    'gameborrow:add',
                    room_id=self.request.matchdict['room_id'],
                    obj_id=self.obj.GameEntity.id),
            })
        else:
            return ''

    @has_access_to_route('gamecopy:movetobox')
    def move_to_box(self):
        if not self.obj.GameEntity.is_in_box:
            return self.render_for('move_to_box_button.haml', {
                'url': self.route(
                    'gamecopy:movetobox',
                    room_id=self.request.matchdict['room_id'],
                    obj_id=self.obj.GameEntity.id,
                ),
                'game': self,
            })
        else:
            return ''

    def get_list_class(self):
        if self.obj.GameEntity.is_in_box:
            return 'warning'
        elif not self.obj.GameEntity.is_avalible():
            return "danger"
        elif self.obj.GameEntity.active_borrows_len() == 0:
            return 'success'
        else:
            return "info"

    def info(self):
        return self.render_for('info.haml', {
            'game': self.obj.Game,
        })
