# -*- coding:utf-8 -*-

"""a colorful terminate from celery! support unix and py2 only"""
from __future__ import unicode_literals
import os, sys, platform
from functools import reduce, partial

COLOR_SET = dict(zip(["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"], range(8)))
STYLE_SET = {"bold": 1, "underline": 4, "blink": 5, "reverse": 7, "bright": 8}
OP_SEQ = '\033[%dm'
RESET_SEQ = '\033[0m'
COLOR_SEQ = '\033[1;%dm'

# tmux requires unrecognized OSC sequences to be wrapped with DCS tmux;
# <sequence> ST, and for all ESCs in <sequence> to be replaced with ESC ESC.
# It only accepts ESC backslash for ST.
ITERM_PROFILE = os.environ.get('ITERM_PROFILE')
TERM = os.environ.get('TERM')
TERM_IS_SCREEN = TERM and TERM.startswith('screen')
_IMG_PRE = '\033Ptmux;\033\033]' if TERM_IS_SCREEN else '\033]'
_IMG_POST = '\a\033\\' if TERM_IS_SCREEN else '\a'

IS_WINDOWS = platform.system() == 'Windows'

def fg(s):
    return COLOR_SEQ % s

string = str

class Colored(object):
    """Terminal colored text.

    Example:
        >>> c = colored(enabled=True)
        >>> print(str(c.red('the quick '), c.blue('brown ', c.bold('fox ')),
        ...       c.magenta(c.underline('jumps over')),
        ...       c.yellow(' the lazy '),
        ...       c.green('dog ')))
    """

    def __init__(self, *s, **kwargs):
        """
        key in kwargs:
            enable -> enable the color terminate
            op     -> unknown now
        """
        self.s = s
        self.enabled = not IS_WINDOWS and kwargs.get("enable", True)
        self.op = kwargs.get("op", "")
        self._colorful()
        self._style()

    def _colorful(self):
        def func(base, c, *s):
            return self.node(s, fg(base+c))
        prefix = [(40, "i"), (30, ""), ]
        names = {}
        for c in COLOR_SET:
            for base, pre in prefix:
                lc = c.lower()
                f = partial(func, c=c, base=base)
                setattr(self, lc, f)
            names[lc] = f
        self.names = names

    def _style(self):
        def func(c, *s):
            return self.node(s, OP_SEQ % c)
        for c in STYLE_SET:
            f = partial(func, c=c)
            setattr(self, c.lower(), f)

    def _add(self, a, b):
        return string(a) + string(b)

    def _fold_no_color(self, a, b):
        def _(s):
            return s.no_color() if hasattr(s, "no_color") else string(s)
        A = _(a)
        B = _(b)
        return ''.join((string(A), string(B)))

    def __repr__(self):
        return repr(self.no_color())

    def no_color(self):
        if self.s:
            return string(reduce(self._fold_no_color, self.s))
        return ''

    def reset(self, *s):
        return self.node(s or [''], RESET_SEQ)

    def embed(self):
        prefix = ''
        if self.enabled:
            prefix = self.op
        return ''.join((string(prefix), string(reduce(self._add, self.s))))

    def __str__(self):
        suffix = ''
        if self.enabled:
            suffix = RESET_SEQ
        return string(''.join((self.embed(), string(suffix))))

    def __repr__(self):
        return repr(self.no_color())

    def __add__(self, other):
        return string(self) + string(other)

    def node(self, s, op):
        return self.__class__(enabled=self.enabled, op=op, *s)


__all__ = ["Colored"]