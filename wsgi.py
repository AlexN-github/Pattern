import json
import datetime

from templator import render


def contacts_view(params, method):
    def save_user_message(params):
        now = datetime.datetime.now()
        dt_str = now.strftime("%d-%m-%Y %H:%M:%S")
        message_dict = '{0}\r\n'.format(json.dumps(params))
        with open("user_messages.txt", "a") as text_file:
            text_file.write("{0}::Message from user: {1}".format(dt_str, message_dict))
        return

    if method == 'GET':
        output = render('contacts.html', params=params)
    elif method == 'POST':
        save_user_message(params)
        output = render('contacts.html', params=params, result_message='Сообщение успешно отправлено')
    else:
        return '405 ERROR', [b'Unsupport method']

    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def index_view(params, method):
    output = render('main.html', params=params)
    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def authors_view(params, method):
    output = render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}], params=params)
    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def about_view(params, method):
    output = render('about.html', params=params)
    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def not_found_404_view(params, method):
    return '404 WHAT', [b'404 PAGE Not Found']


class Other:
    def __call__(self, params):
        print(params)
        return '200 OK', [b'<h1>other</h1>']


routes = {
    '/': index_view,
    '/authors/': authors_view,
    '/about/': about_view,
    '/contacts/': contacts_view,
    '/other/': Other(),
    '': not_found_404_view
}


# Front controllers
def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path in self.routes:
            view = self.routes[path]
        else:
            view = self.routes['']
        request = {}
        params = self.get_parameters(environ)
        # run front controller
        for front in self.fronts:
            front(request)
        method = environ['REQUEST_METHOD']
        code, body = view(params=params, method=method)
        # run page controller
        start_response(code, [('Content-Type', 'text/html')])
        return body

    def get_parameters(self, environ):
        def convert_to_dict(data: str):
            result = {}
            if data:
                # делим параметры через &
                params = data.split('&')
                for item in params:
                    # делим ключ и значение через =
                    k, v = item.split('=')
                    result[k] = v
            return result

        def parse_post_params(env) -> bytes:
            # получаем длину тела
            content_length_data = env.get('CONTENT_LENGTH')
            # приводим к int
            content_length = int(content_length_data) if content_length_data else 0
            # считываем данные, если они есть
            data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
            result = {}
            if data:
                # декодируем данные
                data_str = data.decode(encoding='utf-8')
                # собираем их в словарь
                result = convert_to_dict(data_str)
            return result

        # получаем параметры запроса
        #print(environ)
        method = environ['REQUEST_METHOD']
        if method == 'POST':
            params = parse_post_params(environ)

        else:
            query_string = environ['QUERY_STRING']
            # превращаем параметры в словарь
            params = convert_to_dict(query_string)

        return params


application = Application(routes, fronts)
