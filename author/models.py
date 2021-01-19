from django.db import models, IntegrityError, DataError
from django.urls import reverse


class Author(models.Model):

    name = models.CharField(blank=True, max_length=20)
    surname = models.CharField(blank=True, max_length=20)
    patronymic = models.CharField(blank=True, max_length=20)
    bio = models.TextField(blank=True)
    photo = models.ImageField(null=True, blank=True, default='default_author.png')

    def author_photo_or_default(self, default_path="default_author.png"):
        if self.photo:
            return self.photo.url
        return default_path

    def __str__(self):
        return f'{self.name}, {self.surname} ({self.patronymic})'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def get_by_id(author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            raise Exception("Author does not exist.")
        else:
            return author

    @staticmethod
    def delete_by_id(author_id):
        try:
            obj = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            pass
        else:
            obj.delete()
            return True
        return False

    @staticmethod
    def create(name, surname, patronymic, bio, photo):
        try:
            author = Author(name=name, surname=surname, patronymic=patronymic, bio=bio, photo=photo)
            author.save()
        except (IntegrityError, DataError):
            pass
        else:
            return author

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
        }

    def update(self,
               name=None,
               surname=None,
               patronymic=None,
               bio=None,
               photo=None):
        if name and isinstance(name, str):
            self.name = name
        if surname and isinstance(surname, str):
            self.surname = surname
        if patronymic and isinstance(patronymic, str):
            self.patronymic = patronymic
        if bio and isinstance(bio, str):
            self.bio = bio
        if photo:
            print(photo)
            self.photo = photo
        self.save()

    @staticmethod
    def get_all():
        all_authors = list(Author.objects.all())
        return all_authors

    def get_absolute_url(self):
        return reverse('author_by_id', kwargs={'id': self.id})
