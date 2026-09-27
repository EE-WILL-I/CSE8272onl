from django.core.management.base import BaseCommand
from library.models import Author, Category, Book


CATEGORIES = [
    {'name': 'Fiction',  'slug': 'fiction'},
    {'name': 'Science',  'slug': 'science'},
    {'name': 'History',  'slug': 'history'},
]

AUTHORS = [
    {'name': 'George Orwell',        'bio': 'English novelist and essayist.'},
    {'name': 'Carl Sagan',           'bio': 'Astronomer and science communicator.'},
    {'name': 'Yuval Noah Harari',    'bio': 'Israeli historian and author.'},
    {'name': 'Frank Herbert',        'bio': 'American science fiction author.'},
    {'name': 'Stephen Hawking',      'bio': 'Theoretical physicist and cosmologist.'},
]

BOOKS = [
    {'title': '1984',                        'author': 'George Orwell',     'category': 'fiction',  'year': 1949, 'description': 'A dystopian novel set in a totalitarian state where Big Brother watches everyone.', 'available': True},
    {'title': 'Animal Farm',                  'author': 'George Orwell',     'category': 'fiction',  'year': 1945, 'description': 'A satirical allegory about the corrupting nature of power.', 'available': True},
    {'title': 'Cosmos',                       'author': 'Carl Sagan',        'category': 'science',  'year': 1980, 'description': 'A journey through the universe exploring space, time, and life.', 'available': True},
    {'title': 'Pale Blue Dot',                'author': 'Carl Sagan',        'category': 'science',  'year': 1994, 'description': 'Reflections on the future of humanity in space.', 'available': False},
    {'title': 'Sapiens',                      'author': 'Yuval Noah Harari', 'category': 'history',  'year': 2011, 'description': 'A brief history of humankind from the Stone Age to the present.', 'available': True},
    {'title': 'Homo Deus',                    'author': 'Yuval Noah Harari', 'category': 'history',  'year': 2015, 'description': 'A look at the future of humanity and its next goals.', 'available': True},
    {'title': 'Dune',                         'author': 'Frank Herbert',     'category': 'fiction',  'year': 1965, 'description': 'Epic science fiction set on the desert planet Arrakis.', 'available': True},
    {'title': 'Dune Messiah',                 'author': 'Frank Herbert',     'category': 'fiction',  'year': 1969, 'description': 'Sequel to Dune, following Paul Atreides on Arrakis.', 'available': False},
    {'title': 'A Brief History of Time',      'author': 'Stephen Hawking',   'category': 'science',  'year': 1988, 'description': 'An accessible introduction to cosmology and the universe.', 'available': True},
    {'title': 'The Universe in a Nutshell',   'author': 'Stephen Hawking',   'category': 'science',  'year': 2001, 'description': 'A follow-up exploring the frontiers of theoretical physics.', 'available': True},
]


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        if Book.objects.exists():
            self.stdout.write('Database already has data. Skipping seed.')
            return

        cats = {}
        for c in CATEGORIES:
            obj, _ = Category.objects.get_or_create(slug=c['slug'], defaults={'name': c['name']})
            cats[c['slug']] = obj

        authors = {}
        for a in AUTHORS:
            obj, _ = Author.objects.get_or_create(name=a['name'], defaults={'bio': a['bio']})
            authors[a['name']] = obj

        for b in BOOKS:
            Book.objects.create(
                title=b['title'],
                author=authors[b['author']],
                category=cats[b['category']],
                year=b['year'],
                description=b['description'],
                available=b['available'],
            )

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(BOOKS)} books, {len(AUTHORS)} authors, {len(CATEGORIES)} categories.'))
