from django.db import models, IntegrityError, DataError
from django.shortcuts import reverse
from author.models import Author


class Book(models.Model):
    """
        This class represents an Author. \n
        Attributes:
        -----------
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        param authors: list of Authors
        type authors: list->Author
    """

    name = models.CharField(blank=True, max_length=128)
    description = models.TextField(blank=True)
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField(Author, related_name='books')
    stars = models.IntegerField(default=0)
    cover = models.ImageField(upload_to='books_cover', default='default_book.png', blank=True, null=True)

    def book_cover_or_default(self, default_path="default_book.png"):
        if self.cover:
            return self.cover.url
        return default_path

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        return str(self.to_dict())[1:-1]

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def get_by_id(book_id):
        """
        :param book_id: SERIAL: the id of a Book to be found in the DB
        :return: book object or None if a book with such ID does not exist
        """
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise Exception("Book does not exist.")
        else:
            return book

    @staticmethod
    def delete_by_id(book_id):
        """
        :param book_id: an id of a book to be deleted
        :type book_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            obj = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            pass
        else:
            obj.delete()
            return True
        return False

    @staticmethod
    def create(name, description, cover, count=10, authors=None):
        """
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        param authors: list of Authors
        type authors: list->Author
        :return: a new book object which is also written into the DB
        """
        try:
            book = Book(name=name, description=description, cover=cover, count=count, stars=0)
            book.save()
            if authors:
                for author in authors:
                    book.authors.add(author)
                book.save()
            if cover:
                book.cover = cover
                book.save()
        except (IntegrityError, DataError):
            pass
        else:
            return book

    def to_dict(self):
        """
        :return: book id, book name, book description, book count, book authors
        :Example:
        | {
        |   'id': 8,
        |   'name': 'django book',
        |   'description': 'bla bla bla',
        |   'count': 10',
        |   'authors': []
        | }
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'stars': self.stars,
            'authors': [author.id for author in self.authors.all()],
        }

    def update(self, name=None, description=None, count=None, authors=None, cover=None):
        """
        Updates book in the database with the specified parameters.\n
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        :return: None
        """
        if name and isinstance(name, str) and len(name) <= 128:
            self.name = name
        if description and isinstance(description, str):
            self.description = description
        if count and isinstance(count, int):
            self.count = count
        if authors:
            for author in authors:
                self.authors.add(author)
        if cover:
            self.cover = cover
        self.save()

    def add_authors(self, authors):
        """
        Add  authors to  book in the database with the specified parameters.\n
        param authors: list authors
        :return: None
        """
        if authors:
            for author in authors:
                self.authors.add(author)
            self.save()

    def remove_authors(self, authors):
        """
        Remove authors to  book in the database with the specified parameters.\n
        param authors: list authors
        :return: None
        """
        for author in authors:
            self.authors.remove(author)
        self.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all books
        """
        return Book.objects.all()

    def get_absolute_url(self):
        return reverse('book_by_id', kwargs={'id': self.id})
