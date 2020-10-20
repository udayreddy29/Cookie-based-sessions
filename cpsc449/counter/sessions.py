import logging
import uuid

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from flask import request, jsonify
import requests


class SessionStore:

    def __init__(self, logger=None):
        if logger is None:
            self.logger = logging.getLogger("__name__")
        else:
            self.logger = logger

    def set_key(self, key, value):
        self.logger.debug("set_key('%s', '%s')", key, value)
        raise NotImplementedError()

    def get_key(self, key):
        self.logger.debug("get_key('%s')", key)
        raise NotImplementedError()

    def delete_key(self, key):
        self.logger.debug("delete_key('%s')", key)
        raise NotImplementedError()


class KeyValueSessionStore(SessionStore):

    def __init__(self, url, logger=None):
        super().__init__(logger)
        self.logger.debug('url is %s', url)

    def set_key(self, key, value):
        current = self.get_key(key)
        t = current.get('count', 0)
        self.logger.debug("value of t is '%s'", type(t))
        if t == None:
            payload = {
                key: 1
            }
        else:
            payload = {
                key: t + 1
            }
        r = requests.post("http://localhost:5100/", data=payload)
        self.logger.debug(" after set key '%s'", r.json())
    
    def get_key(self, key):
        url = 'http://localhost:5100/' + key
        r = requests.get(url)
        self.logger.debug("get key '%s'", r.json())
        count = r.json().get(key)
        if count == None:
            return {
                'count' : 0
            }
        return {
            'count': int(count)
        }


class ServerSideSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None):

        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.modified = False


class ServerSideSessionInterface(SessionInterface):

    def __init__(self, session_store):
        self.session_store = session_store

    def _update_session(self, app, session, response):
        self.session_store.set_key(session.sid, dict(session))
        response.set_cookie(
            app.session_cookie_name,
            session.sid,
            expires=self.get_expiration_time(app, session),
            httponly=self.get_cookie_httponly(app),
            domain=self.get_cookie_domain(app),
            path=self.get_cookie_path(app),
            secure=self.get_cookie_secure(app)
        )

    def _delete_session(self, app, response, sid):
        response.delete_cookie(
            app.session_cookie_name,
            domain=self.get_cookie_domain(app),
            path=self.get_cookie_path(app)
        )
        self.session_store.delete_key(sid)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            # Create a session object with a new session id
            sid = str(uuid.uuid4())
            return ServerSideSession(sid=sid)

        data = self.session_store.get_key(sid)

        if data:
            # Create a session object with existing data
            return ServerSideSession(data, sid=sid)

        # create an empty session object
        return ServerSideSession(sid=sid)

    def save_session(self, app, session, response):

        if not session:
            if session.modified:
                self._delete_session(app, response, session.sid)
            return

        if self.should_set_cookie(app, session):
            self._update_session(app, session, response)
