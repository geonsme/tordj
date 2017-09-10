
import sys
from tordj.conf import settings
from . import server

class Conf(object):

    @property
    def conf(self):
        module = self.__class__.__module__
        conf = settings.GRPC_SERVICES.get(module)
        if not conf:return {}
        return conf
        

class RegService(type):
    """registered service"""

    def __new__(cls, name, bases, attrs):
        base_service = bases[0]
        base_module = sys.modules[base_service.__module__]
        base_clsname = base_service.__name__
        register_func = getattr(base_module, "add_%s_to_server" % base_clsname)
        subcls_module = "%s.%s" % (attrs["__module__"], name)
        server.SERVICES.append( (register_func, subcls_module) )
        return super(RegService, cls).__new__(cls, name, bases + (Conf,), attrs)
