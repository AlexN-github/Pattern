from framework_wsgi.wsgi import * #Application


# Front controllers
#from models import TrainingSite
from mappers import MapperRegistry
from models import TrainingSite, EmailNotifier, SmsNotifier
from patterns.unitofwork import UnitOfWork
from urls import urls

# Создание копирование курса, список курсов
# Регистрация пользователя, список пользователей
# Логирование

#site = TrainingSite()
#logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

application = Application(urls, fronts)
#application = FakeApplication(urls, fronts)

#application = DebugApplication(urls, fronts)

