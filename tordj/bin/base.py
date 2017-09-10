# -*- coding:utf-8 -*-

"""base for cmd"""
from __future__ import print_function
import re, argparse, sys
import random, os, logging

from .exceptions import Error, EX_OK


class Command(object):

    Parser = argparse.ArgumentParser
    Error = Error
    Description = ""

    #: Name of argparse option used for parsing positional args.
    args_name = 'args'

    def __init__(self,stdout=sys.stdout, 
        stderr=sys.stderr, quiet=False):
        self.stdout = stdout
        self.stderr = stderr
        self.quiet = quiet
        logging.basicConfig()
        self.logger = logging.getLogger("tornado.application")

    def __call__(self, *args, **kwargs):
        random.seed()  # maybe we were forked.
        try:
            ret = self.run(*args, **kwargs)
            return ret if ret is not None else EX_OK
        except self.Error as exc:
            self.on_error(exc)
            return exc.status

    def execute_from_command_line(self, argv=None):
        if argv is None:
            argv = list(sys.argv)
        self.prog_name = os.path.basename(argv[1])
        return self.handle_argv(self.prog_name, argv[2:])

    def run(self, *args, **kwargs):
        raise NotImplementedError('subclass responsibility')

    def add_arguments(self, parser):
        pass

    def add_preload_arguments(self, parser):
        pass

    def create_parser(self, prog_name):
        parser = self.Parser(prog=prog_name,
                             formatter_class=argparse.RawDescriptionHelpFormatter,
                             description = self.Description
                             )
        self.add_preload_arguments(parser)
        self.add_arguments(parser)
        self.parser = parser
        return parser

    def handle_argv(self, prog_name, argv, command=None):
        """Parse arguments from argv and dispatch to :meth:`run`.

        Warning:
            Exits with an error message if :attr:`supports_args` is disabled
            and ``argv`` contains positional arguments.

        Arguments:
            prog_name (str): The program name (``argv[0]``).
            argv (List[str]): Rest of command-line arguments.
        """
        options, args = self.prepare_args(
            *self.parse_options(prog_name, argv, command))
        return self(*args, **options)

    def parse_options(self, prog_name, arguments, command=None):
        """Parse the available options."""
        # Don't want to load configuration to just print the version,
        # so we handle --version manually here.
        self.parser = self.create_parser(prog_name)
        options = vars(self.parser.parse_args(arguments))
        return options, options.pop(self.args_name, None) or []

    def prepare_args(self, options, args):
        if options:
            options = {
                k: self.expanduser(v)
                for k, v in options.items() if not k.startswith('_')
            }
        args = [self.expanduser(arg) for arg in args]
        return options, args

    def on_error(self, exc):
        self.logger.error(exc)

    def expanduser(self, v):
        if type(v) in [str, unicode]:
            return os.path.expanduser(v)
        else:
            return v

