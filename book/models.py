from django.db import models, IntegrityError, DataError
from django.shortcuts import reverse
from author.models import Author


class Book(models.Model):

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
        return f'{self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def get_by_id(book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise Exception("Book does not exist.")
        else:
            return book

    @staticmethod
    def delete_by_id(book_id):
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
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'stars': self.stars,
            'authors': [author.id for author in self.authors.all()],
        }

    def update(self, name=None, description=None, count=None, authors=None, cover=None):
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
        if authors:
            for author in authors:
                self.authors.add(author)
            self.save()

    def remove_authors(self, authors):
        for author in authors:
            self.authors.remove(author)
        self.save()

    @staticmethod
    def get_all():
        return Book.objects.all()

    def get_absolute_url(self):
        return reverse('book_by_id', kwargs={'id': self.id})
