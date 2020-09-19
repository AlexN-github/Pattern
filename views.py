import datetime
import json

from render import render


def contacts_view(params, method):
    def save_user_message(params):
        now = datetime.datetime.now()
        dt_str = now.strftime("%d-%m-%Y %H:%M:%S")
        message_dict = '{0}\r\n'.format(json.dumps(params))
        with open("user_messages.txt", "a", encoding="utf-8") as text_file:
            text_file.write("{0}::Message from user: {1}".format(dt_str, message_dict))
        return

    context = {
        'title': 'Контакты',
        'params': params
    }
    if method == 'GET':
        output = render('contacts.html', context=context)
    elif method == 'POST':
        save_user_message(params)
        context['result_message'] = 'Сообщение успешно отправлено'
        output = render('contacts.html', context=context)
    else:
        return '405 ERROR', [b'Unsupport method']

    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def index_view(params, method):
    context = {
        'title': 'Главная страница сайта!!!',
        'params': params
    }
    output = render('index.html', context=context)
    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def authors_view(params, method):
    context = {
        'title': 'Авторы!!!',
        'object_list': [{'name': 'Leo'}, {'name': 'Kate'}],
        'params': params
    }
    output = render('authors.html', context=context)
    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def about_view(params, method):
    context = {
        'title': 'О проекте!!!',
        'params': params
    }
    output = render('about.html', context=context)
    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def not_found_404_view(params, method):
    return '404 WHAT', [b'404 PAGE Not Found']


class Other:
    def __call__(self, params):
        print(params)
        return '200 OK', [b'<h1>other</h1>']

