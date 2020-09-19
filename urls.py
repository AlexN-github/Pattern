from views import *

urls = {
    '/': index_view,
    '/authors/': authors_view,
    '/about/': about_view,
    '/contacts/': contacts_view,
    '/other/': Other(),
    '': not_found_404_view
}