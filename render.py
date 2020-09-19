from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from jinja2 import Template


# def render(template_name, **kwargs):
#     with open(template_name, encoding='utf-8') as f:
#         template = Template(f.read())
#     # рендерим шаблон с параметрами
#     return template.render(**kwargs)

def render(template_name, folder='templates', **kwargs):
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)


if __name__ == '__main__':
    #output_test = render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    output_test = render('index.html')
    print(output_test)