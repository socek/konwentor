class FlashMessage(object):

    def __init__(self, message=None, msgtype=None):
        self.message = message
        self.msgtype = msgtype

    def to_dict(self):
        return {
            'message': self.message,
            'msgtype': self.msgtype,
        }

    def from_dict(self, data):
        self.message = data['message']
        self.msgtype = data['msgtype']
