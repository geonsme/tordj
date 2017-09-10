# -*- coding: utf-8 -*-

import sys, os
from tordj.conf import settings


class BaseEngine(object):

    template_dirname = None

    def __init__(self, **params):
        self.dirs = list(params.get("DIRS", []))
        self.app_dirs = bool(params.get("APP_DIRS", []))
        self._dir_cache = []

    @property
    def template_dirs(self):
        if self._dir_cache:
            return tuple(self.dirs) + self._dir_cache
        template_dirs = tuple(self.dirs)
        if self.app_dirs:
            template_dirs += self._get_app_template_dirs()
        return template_dirs

    def _get_app_template_dirs(self):
        assert self.template_dirname, "template_dirname must be specified in subclass of BaseEngine"
        for app in settings.INSTALLED_APPS:
            module = sys.modules.get(app)
            if not module:
                raise RuntimeError("App doesn't be loaded yet!")
            app_dir = os.path.abspath(os.path.dirname(module.__file__))
            template_dir = os.path.join(app_dir, self.template_dirname)
            if os.path.isdir(template_dir):
                self._dir_cache.append(template_dir)
        return tuple(self._dir_cache)

