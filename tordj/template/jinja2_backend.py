# -*- coding: utf-8 -*-

import tornado.template
from tordj.conf import settings
from tordj.utils.module_loading import import_string
from . import BaseEngine


def override_render(template_cls):
    """add `generate` method to template_cls"""
    return type("TemplateCls", (template_cls, ), {"generate": template_cls.render})


class Jinja2Engine(BaseEngine, tornado.template.BaseLoader):

    template_dirname = "jinja2"

    def __init__(self, params):
        import jinja2
        params = params.copy()
        options = params.pop('OPTIONS').copy()
        BaseEngine.__init__(self, **params)
        tornado.template.BaseLoader.__init__(self)
        #super(Jinja2Engine, self).__init__(**params)

        environment = options.pop('environment', 'jinja2.Environment')
        environment_cls = import_string(environment)
        environment_cls.template_class = override_render(jinja2.Template)

        if 'loader' not in options:
            options['loader'] = jinja2.FileSystemLoader(self.template_dirs)
        options.setdefault('autoescape', True)
        options.setdefault('auto_reload', settings.DEBUG)
        options.setdefault('undefined',
                           jinja2.DebugUndefined if settings.DEBUG else jinja2.Undefined)
        self.env = environment_cls(**options)

    def resolve_path(self, name, parent_path=None):
        return name 

    def _create_template(self, name):
        return self.env.get_template(name)