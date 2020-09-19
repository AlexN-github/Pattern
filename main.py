from framework_wsgi.wsgi import Application


# Front controllers
from urls import urls


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

application = Application(urls, fronts)
