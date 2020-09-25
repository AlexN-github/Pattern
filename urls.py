from views import *

urls = {
    '/': index_view,
    '/list-course/': list_course,
    '/create-course/': create_course,
    '/copy-course/': copy_course,
    '/list-category/': list_category,
    '/create-category/': create_category,
    '/authors/': authors_view,
    '/about/': about_view,
    '/contacts/': contacts_view,
    '/other/': Other(),
    '': not_found_404_view
}

