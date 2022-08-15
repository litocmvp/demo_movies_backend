class AppErrorBaseClass(Exception):
    pass
class ObjectNotFound(AppErrorBaseClass):
    pass

class ObjectForbidden(AppErrorBaseClass):
    pass

class ObjectUnauthorized(AppErrorBaseClass):
    pass

