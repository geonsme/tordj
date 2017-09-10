from __future__ import absolute_import
from tordj import session

class SetupSession(object):

    def process_request(self, handler):
        handler.session = session.Session(handler.application.session_store, handler)

    def process_response(self, handler):
        handler.session.save()
