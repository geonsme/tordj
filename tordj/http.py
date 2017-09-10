from __future__ import absolute_import
import tornado
from tornado.web import RequestHandler, Application
from .conf import settings
from .utils.module_loading import import_string

def import_middleware():
    MIDDLEWARES = getattr(settings, "MIDDLEWARE", [])
    ret = []
    for m in MIDDLEWARES:
        middleware_cls = import_string(m)
        ret.append(middleware_cls())
    return ret

MIDDLEWARES = import_middleware()


class BaseHandler(RequestHandler):

    def prepare(self):
        for middleware in MIDDLEWARES:
            if hasattr(middleware, "process_request"):
                middleware.process_request(self)
        super(BaseHandler, self).prepare()

    def finish(self, chunk=None):
        for middleware in reversed(MIDDLEWARES):
            if hasattr(middleware, "process_response"):
                middleware.process_response(self)
        super(BaseHandler, self).finish(chunk)

    def write_error(self, status_code, **kwargs):
        for middleware in MIDDLEWARES:
            if hasattr(middleware, "process_exception"):
                exc_info = kwargs["exc_info"]
                middleware.process_exception(self, exc_info)
        super(BaseHandler, self).write_error(status_code, **kwargs)

    def get_current_user(self):
        return self.session.get("authenticated_user", None)


class App(Application):
    
    def __init__(self, *args, **kwargs):
        from tordj import session
        from . import loader
        from .loader import ApplicationLoader, TemplateLoader
        self.session_store = session.SessionRedisStore()
        
        handlers = loader.ApplicationLoader().routers
        template_loader = loader.TemplateLoader().engine
        handlers += loader.StaticFileLoader().static_handlers
        cookie_secret = settings.COOKIE_SECRET
        super(App, self).__init__(handlers=handlers, 
                                  template_loader=template_loader, 
                                  cookie_secret=cookie_secret,
                                  **settings.TONADO_CONFIG
                                 )

    def start(self):
        tornado.ioloop.IOLoop.instance().start()



__all__ = [ "BaseHandler", "App", ]