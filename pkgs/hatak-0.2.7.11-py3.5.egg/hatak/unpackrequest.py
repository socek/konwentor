class UnpackRequest(object):

    def __init__(self):
        self.unpackers = {}

    def add(self, name, method):
        self.unpackers[name] = method

    def generate_property(self, unpacker):
        return property(lambda self: unpacker(self.request))

    def __call__(self, obj):
        for key, unpacker in self.unpackers.items():
            prop = self.generate_property(unpacker)
            setattr(obj.__class__, key, prop)


def unpack(obj, request):
    obj.request = request
    request.registry['unpacker'](obj)
