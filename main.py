from framework_wsgi.wsgi import Application


# Front controllers
from models import TrainingSite
from urls import urls

# Создание копирование курса, список курсов
# Регистрация пользователя, список пользователей
# Логирование


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

application = Application(urls, fronts)
