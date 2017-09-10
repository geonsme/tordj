# -*- coding: utf-8 -*
import os, sys
from tordj.conf import settings
from tordj.utils.module_loading import import_string

class TemplateLoader(object):

    def __init__(self):
        self._engines = []

    @property
    def engine(self):
        if self._engines: return self._engines
        for template in settings.TEMPLATES:
            template = template.copy()
            backend = template.pop("BACKEND")
            backend_cls = import_string(backend)
            engine = backend_cls(template)
            self._engines.append(engine)
        return self._engines[0]


class ApplicationLoader(object):


    def __init__(self):
        self._installed = []

    @property
    def apps(self):
        for app in settings.INSTALLED_APPS:
            app_module = import_string(app)
            self._installed.append(app_module)
        return self._installed

    @property
    def routers(self):
        router_list = []
        for app in self.apps:
            router_module = app.__name__ + ".%s" % settings.ROUTER_MODULE
            router_list += import_string(router_module)
        return router_list

    def load(self):
        return self.routers


class StaticFileLoader(object):

    @property
    def static_handlers(self):
        if not settings.DEBUG:
            return []
        from tornado.web import StaticFileHandler
        ret = []
        static_prefix = settings.STATIC_URL
        if settings.STATIC_PATH and os.path.isdir(settings.STATIC_PATH):
            return [(r"%s(.*)" % static_prefix, StaticFileHandler, {"path": settings.STATIC_PATH})]
        for app in settings.INSTALLED_APPS:
            label = app.rpartition(".")[2]
            regex = r"%s%s/(.*)" % (static_prefix, label)
            module = sys.modules.get(app)
            if not module:
                raise RuntimeError("App doesn't be loaded yet!")
            app_dir = os.path.abspath(os.path.dirname(module.__file__))
            path = os.path.join(app_dir, settings.STATIC_FOLDERNAME + "/" + label)
            ret.append( (regex, StaticFileHandler, {"path": path}) )
        return ret
