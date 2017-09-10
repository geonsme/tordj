# -*- coding: utf-8 -*-
import uuid, hmac
import hashlib
from .conf import settings
from .utils.module_loading import import_string

class InvalidSessionException(Exception):pass


class SessionData(dict):

    def __init__(self, session_id, hmac_key):
        self.session_id = session_id
        self.hmac_key = hmac_key

    def __getstate__(self):
        return self


class Session(SessionData):

    def __init__(self, session_store, request_handler):
        self._store = session_store
        self._handler = request_handler
        try:
            session = session_store.get(request_handler)
        except InvalidSessionException:
            session = session_store.get()
        self.update(session)
        super(Session, self).__init__(session.session_id, session.hmac_key)

    def save(self):
        self._store.set(self._handler, self)
        

class SessionRedisStore(object):

    def __init__(self, store_option={}, secret_key=None, expire=None):
        if not secret_key:
            secret_key = getattr(settings, "SECRET_KEY")
        if not expire:
            expire = getattr(settings, "SESSION_COOKIE_AGE", 15*60)
        if not store_option:
            store_option = getattr(settings, "DATABASES")["session"]["OPTIONS"]
        self.secret_key = secret_key
        self.session_age = expire
        try:
            import redis
            self.redis = redis.StrictRedis(**store_option)
            #import tornadoredis
            #self.redis = tornadoredis.Client(**store_option)
            #self.redis.connect()
        except ImportError:
            raise RuntimeError("redis session store rely on redis library, please execute `pip install redis` to install this lib")
        except Exception, e:
            print e
            raise RuntimeError("cannot connect redis with!! please check database config and redis server status!")
        
    def _fetch(self, session_id):
        serializer = import_string(settings.SESSION_SERIALIZER)
        raw_data = self.redis.get(session_id)
        if raw_data:
            #self.redis.setex(session_id, self.session_age, raw_data)
            session_data = serializer.loads(raw_data)
        else:
            session_data = {}
        return session_data

    def get(self, request_handler=None):
        if not request_handler:
            session_id = None
            hmac_key = None
        else:
            session_id = request_handler.get_secure_cookie(settings.SESSION_COOKIE_NAME)
            hmac_key = request_handler.get_secure_cookie(settings.SESSION_COOKIE_HMAC_NAME)
        if not session_id:
            exists = False
            session_id = self._generate_id()
            hmac_key = self._generate_hmac(session_id)
        else:
            exists = True
        check_hmac = self._generate_hmac(session_id)
        if hmac_key != check_hmac:
            raise InvalidSessionException()
        session = SessionData(session_id, hmac_key)
        if exists:
            session_data = self._fetch(session_id)
            session.update(session_data)
        return session

    def set(self, request_handler, session):
        request_handler.set_secure_cookie(settings.SESSION_COOKIE_NAME, session.session_id)
        request_handler.set_secure_cookie(settings.SESSION_COOKIE_HMAC_NAME, session.hmac_key)
        serializer = import_string(settings.SESSION_SERIALIZER)
        raw_data = serializer.dumps(session)
        self.redis.setex(session.session_id, self.session_age, raw_data)

    def _generate_id(self):
        new_id = hashlib.sha256(self.secret_key + str(uuid.uuid4()))
        return new_id.hexdigest()

    def _generate_hmac(self, session_id):
        return hmac.new(session_id, self.secret_key, hashlib.sha256).hexdigest()



