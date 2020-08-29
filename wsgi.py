from templator import render


def index_view(request):
    output = render('main.html')
    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def authors_view(request):
    output = render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def about_view(request):
    output = render('about.html')
    b_output = bytes(output, encoding='utf-8')
    return '200 OK', [b_output]


def not_found_404_view(request):
    return '404 WHAT', [b'404 PAGE Not Found']


class Other:
    def __call__(self, request):
        print(request)
        return '200 OK', [b'<h1>other</h1>']


routes = {
    '/': index_view,
    '/authors/': authors_view,
    '/about/': about_view,
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
        print('work')
        path = environ['PATH_INFO']
        if path in self.routes:
            view = self.routes[path]
        else:
            view = self.routes['']
        request = {}
        # run front controller
        for front in self.fronts:
            front(request)
        code, body = view(request)
        # run page controller
        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(routes, fronts)

