import tornado
import tornado.web
import tornadio2
import json
from tornadio2 import TornadioRouter, SocketServer
from django.core.management.base import NoArgsCommand
from django.contrib.auth import get_user as _get_user
from django.utils.importlib import import_module
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def get_session(session_id):
    engine = import_module(settings.SESSION_ENGINE)
    return engine.SessionStore(session_id)


def get_user(session):
    class Dummy(object):
        pass
    django_request = Dummy()
    django_request.session = session
    return _get_user(django_request)


class HttpHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        session = get_session(data['sessionid'])
        user = get_user(session)
        if not user.is_authenticated():
            return
        users_pks = data['users']
        users = None
        if users_pks:
            users = list(User.objects.filter(pk__in=users_pks))
        WSConnection.broadcast(data, users)

    def get(self, *args, **kwargs):
        self.write("OK")


class WSConnection(tornadio2.SocketConnection):

    clients = set()

    def on_open(self, request):
        pass

    def on_message(self, message):
        if message['type'] != 'auth request':
            return
        session = get_session(self.session.info.get_cookie('sessionid').value)
        self.user = get_user(session)
        if self.user.is_authenticated():
            self.clients.add(self)
            self.send({'type': 'auth result',
                       'authorized': self.user.is_authenticated()})

    @classmethod
    def broadcast(cls, data, users=None):
        for client in cls.clients:
            if users and not client.user in users:
                continue
            client.send({'type': 'message',
                         'message': data['message'],
                         'messageId': data['message_id']})

    def __del__(self):
        self.clients.remove(self)


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        application = tornado.web.Application(
            TornadioRouter(WSConnection).apply_routes(
                [(r'/post_message', HttpHandler), ]
            ),
            socket_io_port=8080)
        SocketServer(application)
        raw_input()