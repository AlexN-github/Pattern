
class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        # Если в конце нет '/' то добавляем
        if path[-1] != '/':
            path = path + '/'
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
        return [body.encode('utf-8')]

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


#application = Application(routes, fronts)
