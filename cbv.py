from render import render


class TemplateView:
    template_name = 'template.html'
    title: 'Название страницы'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        print(context)
        return '200 OK', render(template_name, context=context)

    def __call__(self, params, method):
        self.params = params
        self.method = method
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {
                    'title': self.title,
                    context_object_name: queryset
                   }
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    def get_request_data(self) -> dict:
        return self.params

    def create_obj(self, data: dict):
        pass

    def get_context_data(self):
        context = {
                    'title': self.title
                   }
        return context

    def __call__(self, params, method):
        self.params = params
        self.method = method
        if self.method == 'POST':
            # метод пост
            #data = self.get_request_data(params)
            self.create_obj(params)
            # редирект?
            # return '302 Moved Temporarily', render('create_course.html')
            # Для начала можно без него
            return self.render_template_with_context()
        else:
            return super().__call__(self.params, self.method)
