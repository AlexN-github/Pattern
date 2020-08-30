from jinja2 import Template

def render(template_name, **kwargs):
    with open(template_name, encoding='utf-8') as f:
        template =Template(f.read())
    # рендерим шаблон с параметрами
    return template.render(**kwargs)


if __name__ == '__main__':
    #output_test = render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    output_test = render('main.html')
    print(output_test)
