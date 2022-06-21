from django.test import TestCase
from django.urls import reverse

from .models import Author, Book

def create_good_author(name, pseudonym=None):
    return Author.objects.create(
        name=name,
        pseudonym=pseudonym,
        username=name.replace(' ', ''),
        password='asdf'
        )

def create_good_book(title, price, author):
    return Book.objects.create(
        title=title,
        description='Lorum ipsum mango de tango',
        price=price,
        author=author
        )


class AuthorModelTests(TestCase):

    def test_author_required_fields(self):
        """
        ensures that name is required and pseduonym is optional
        """

        new_author = Author()
        with self.assertRaises(Exception):
            new_author.full_clean()

        new_author.name = 'test author'
        with self.assertRaises(Exception):
            new_author.full_clean()

        new_author.username = 'test'
        with self.assertRaises(Exception):
            new_author.full_clean()

        new_author.password = 'asdf'
        new_author.full_clean()

        new_author.pseudonym = 'psuedo'
        new_author.full_clean()


class BookModelTests(TestCase):

    def test_book_required_fields(self):
        """
        ensures that all required fields (title, description
        author and price) are enforced
        """
        new_book = Book()
        with self.assertRaises(Exception):
            new_book.full_clean()

        new_book.title = 'just a title'
        with self.assertRaises(Exception):
            new_book.full_clean()

        new_book.description = 'and a desc'
        with self.assertRaises(Exception):
            new_book.full_clean()

        new_book.price = '13.56'
        with self.assertRaises(Exception):
            new_book.full_clean()

        new_author = Author(name='test author', username = 'test', password = 'asdf')
        new_author.save()
        new_book.author = new_author
        new_book.full_clean()
