import datetime
import json

from logging_mod import logger
from models import site
from render import render


def list_course(params, method):
    context = {
        'title': 'Список курсов',
        'params': params,
        'objects_list': site.courses
    }
    logger.log(context['title'])
    return '200 OK', render('list_course.html', context=context)


def list_category(params, method):
    context = {
        'title': 'Список категорий',
        'params': params,
        'objects_list': site.categories
    }
    logger.log(context['title'])
    return '200 OK', render('list_category.html', context=context)


def create_course(params, method):
    if method == 'POST':
        # метод пост
        print(params)
        name = params['name']
        if 'category_id' in params:
            category_id = params['category_id']
        else:
            category_id = None
        #category_id = data.get('category_id')
        print('category_id = ', category_id)
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            site.courses.append(course)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        context = {
            'title': 'Создать курс',
            'params': params
        }
        logger.log(context['title'])
        return '200 OK', render('create_course.html', context=context)
    else:
        context = {
            'title': 'Создать курс',
            'params': params,
            'categories': site.categories
        }
        logger.log(context['title'])
        return '200 OK', render('create_course.html', context=context)


def create_category(params, method):
    if method == 'POST':
        # метод пост
        print(params)
        name = params['name']
        if 'category_id' in params:
            category_id = params['category_id']
        else:
            category_id = None

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        context = {
            'title': 'Создать категорию',
            'params': params
        }
        logger.log(context['title'])
        return '200 OK', render('create_category.html', context=context)
    else:
        context = {
            'title': 'Создать категорию',
            'params': params,
            'categories': site.categories
        }
        logger.log(context['title'])
        return '200 OK', render('create_category.html', context=context)


def copy_course(params, method):
    name = params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    context = {
        'title': 'Список курсов',
        'params': params,
        'objects_list': site.courses
    }
    logger.log(context['title'])
    return '200 OK', render('list_course.html', context=context)


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
    logger.log(context['title'])
    if method == 'GET':
        output = render('contacts.html', context=context)
    elif method == 'POST':
        save_user_message(params)
        context['result_message'] = 'Сообщение успешно отправлено'
        output = render('contacts.html', context=context)
    else:
        return '405 ERROR', 'Unsupport method'

    return '200 OK', output


def index_view(params, method):
    context = {
        'title': 'Главная страница сайта!!!',
        'params': params
    }
    logger.log(context['title'])
    return '200 OK', render('index.html', context=context)


def authors_view(params, method):
    context = {
        'title': 'Авторы!!!',
        'object_list': [{'name': 'Leo'}, {'name': 'Kate'}],
        'params': params
    }
    return '200 OK', render('authors.html', context=context)


def about_view(params, method):
    context = {
        'title': 'О проекте!!!',
        'params': params
    }
    logger.log(context['title'])
    return '200 OK', render('about.html', context=context)


def not_found_404_view(params, method):
    return '404 WHAT', '404 PAGE Not Found'


class Other:
    def __call__(self, params):
        print(params)
        return '200 OK', '<h1>other</h1>'

