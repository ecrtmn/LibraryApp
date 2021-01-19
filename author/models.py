from django.db import models, IntegrityError, DataError
from django.urls import reverse


class Author(models.Model):
    """
        This class represents an Author. \n
        Attributes:
        -----------
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes last name of the author
        type surname: str max_length=20
        param patronymic: Describes middle name of the author
        type patronymic: str max_length=20

    """

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
        """
        Magic method is redefined to show all information about Author.
        :return: author id, author name, author surname, author patronymic
        """
        return f'{self.name}, {self.surname} ({self.patronymic})'

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Author object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def get_by_id(author_id):
        """
        :param author_id: SERIAL: the id of a Author to be found in the DB
        :return: author object or None if a user with such ID does not exist
        """
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            raise Exception("Author does not exist.")
        else:
            return author

    @staticmethod
    def delete_by_id(author_id):
        """
        :param author_id: an id of a author to be deleted
        :type author_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
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
        """
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: a new author object which is also written into the DB
        """
        try:
            author = Author(name=name, surname=surname, patronymic=patronymic, bio=bio, photo=photo)
            author.save()
        except (IntegrityError, DataError):
            pass
        else:
            return author

    def to_dict(self):
        """
        :return: author id, author name, author surname, author patronymic
        :Example:
        | {
        |   'id': 8,
        |   'name': 'fn',
        |   'surname': 'mn',
        |   'patronymic': 'ln',
        | }
        """
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
        """
        Updates author in the database with the specified parameters.\n
        param name: Describes name of the author
        type name: str max_length=20
        param surname: Describes surname of the author
        type surname: str max_length=20
        param patronymic: Describes patronymic of the author
        type patronymic: str max_length=20
        :return: None
        """
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
        """
        returns data for json request with QuerySet of all authors
        """
        all_authors = list(Author.objects.all())
        return all_authors

    def get_absolute_url(self):
        return reverse('author_by_id', kwargs={'id': self.id})
