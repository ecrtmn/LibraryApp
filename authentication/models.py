from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models, IntegrityError
from django.db.utils import DataError
from django.urls import reverse
from authentication.utils import validate_password

ROLE_CHOICES = (
    (0, 'user'),
    (1, 'staff'),
)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 0)
        # extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 1)
        extra_fields.setdefault('first_name', 'Super')
        extra_fields.setdefault('last_name', 'User')
        extra_fields.setdefault('is_active', True)
        # extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != 1:
            raise ValueError('Superuser must have role=1.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
        This class represents a basic user. \n
        Attributes:
        -----------
        param first_name: Describes first name of the user
        type first_name: str max length=20
        param last_name: Describes last name of the user
        type last_name: str max length=20
        param email: Describes the email of the user
        type email: str, unique, max length=100
        param password: Describes the password of the user
        type password: str
        param created_at: Describes the date when the user was created. Can't be changed.
        type created_at: int (timestamp)
        param updated_at: Describes the date when the user was modified
        type updated_at: int (timestamp)
        param role: user role, default role (0, 'visitor')
        type updated_at: int (choices)
        param is_active: user role, default value False
        type updated_at: bool

    """

    first_name = models.CharField(blank=True, max_length=20)
    last_name = models.CharField(blank=True, max_length=20)
    email = models.EmailField(max_length=100, unique=True, validators=[validate_email])
    password = models.CharField(max_length=128, validators=[validate_password])
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    role = models.IntegerField(default=0, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=False)
    photo = models.ImageField(null=True, blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def user_photo_or_default(self, default_path="default_user.png"):
        if self.photo:
            return self.photo.url
        return default_path

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        :return: user id, user first_name, user last_name,
                 user email, user password, user updated_at, user created_at,
                 user role, user is_active
        """
        return f'{self.first_name}, {self.last_name}'

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise Exception("User does not exist.")
        else:
            return user

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str
        :return: user object or None if a user with such ID does not exist
        """
        try:
            user = CustomUser.objects.get(id=email)
        except CustomUser.DoesNotExist:
            raise Exception("User does not exist.")
        else:
            return user

    @staticmethod
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            obj = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            pass
        else:
            obj.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, last_name=None):
        """
        :param first_name: first name of a user
        :type first_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :return: a new user object which is also written into the DB
        """
        try:
            user = CustomUser(first_name=first_name,
                              last_name=last_name,
                              email=email,
                              is_active=True
                              )
            user.set_password(password)
            validate_email(user.email)
            validate_password(password)
            user.save()
        except (DataError, IntegrityError, AttributeError, ValidationError):
            pass
        else:
            return user

    def to_dict(self):
        """
        :return: user id, user first_name, user last_name,
                 user email, user password, user updated_at, user created_at, user is_active
        :Example:
        | {
        |   'id': 8,
        |   'first_name': 'fn',
        |   'last_name': 'ln',
        |   'email': 'ln@mail.com',
        |   'created_at': 1509393504,
        |   'updated_at': 1509402866,
        |   'role': 0
        |   'is_active:' True
        | }
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'role': self.role,
            'is_active': self.is_active,
        }

    def update(self,
               first_name=None,
               last_name=None,
               password=None,
               role=None,
               is_active=None,
               photo=None,):
        """
        Updates user profile in the database with the specified parameters.\n
        :param first_name: first name of a user
        :type first_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param password: password of a user
        :type password: str
        :param role: role id
        :type role: int
        :param is_active: activation state
        :type is_active: bool
        :return: None
        """
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if password:
            try:
                validate_password(password)
            except ValidationError:
                pass
            else:
                self.password = password
        if role:
            self.role = role
        if is_active:
            self.is_active = is_active
        if photo:
            self.photo = photo
        self.save()


    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all users
        """
        users = CustomUser.objects.all()
        return users

    def get_role_name(self):
        """
        returns str role name
        """
        if self.role:
            return 'staff'
        else:
            return 'user'

    def get_absolute_url(self):
        return reverse('user_by_id', kwargs={'id': self.id})
