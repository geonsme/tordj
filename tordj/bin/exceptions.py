# -*- coding:utf-8 -*-
import os

# exitcodes
EX_OK = getattr(os, 'EX_OK', 0)
EX_FAILURE = 1
EX_USAGE = getattr(os, 'EX_USAGE', 64)

class Error(Exception):
    """Exception raised by commands."""

    status = EX_FAILURE

    def __init__(self, reason, status=None):
        self.reason = reason
        self.status = status if status is not None else self.status
        super(Error, self).__init__(reason, status)

    def __str__(self):
        return self.reason


class UsageError(Error):

    status = EX_USAGE



__all__ = ["Error",]