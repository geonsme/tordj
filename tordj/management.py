# -*- coding: utf-8 -*-

import argparse, sys
from tordj.bin.base import Command
from tordj.utils import module_loading


def all_raise(val):
    raise argparse.ArgumentTypeError("%s is invalid command" % val)

parser = argparse.ArgumentParser(usage="python manage.py <command> [options]")
parser.add_argument("command", help="sub command, it determines what to of this process.", type=all_raise)


class CommandCls(object):

    def __init__(self, subcommand=None):
        self._cls = None
        if not subcommand:
            argv = sys.argv
            if len(argv) <= 1:
                subcommand = "_"
            else:
                subcommand = argv[1]
        self.command = subcommand
        if not self.cls:
            p = parser.parse_args()

    @property
    def cls(self):
        m = self.command
        try:
            module = module_loading.import_module("tordj.bin." + m)
        except ImportError:
            try:
                module = module_loading.import_module(m)
            except ImportError:
                module = None
        c = self._iscommand(module)
        self._cls = c
        return c

    def _iscommand(self, module):
        for attrname in dir(module):
            if not attrname.startswith("__"):
                attr = getattr(module, attrname)
                if isinstance(attr, type) and issubclass(attr, Command) and attr is not Command:
                    return attr
        return None


def execute_from_command_line():

    command_cls = CommandCls().cls
    c = command_cls()
    c.execute_from_command_line()

