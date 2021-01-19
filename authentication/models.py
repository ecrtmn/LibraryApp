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
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 1)
        extra_fields.setdefault('first_name', 'Super')
        extra_fields.setdefault('last_name', 'User')
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('role') != 1:
            raise ValueError('Superuser must have role=1.')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):

    first_name = models.CharField(blank=True, max_length=20)
    last_name = models.CharField(blank=True, max_length=20)
    email = models.EmailField(max_length=100, unique=True, validators=[validate_email])
    password = models.CharField(max_length=128, validators=[validate_password])
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    role = models.IntegerField(default=0, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=False)
    photo = models.ImageField(null=True, blank=True, default='default_user.png')

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def user_photo_or_default(self, default_path="default_user.png"):
        if self.photo:
            return self.photo.url
        return default_path

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def get_by_id(user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise Exception("User does not exist.")
        else:
            return user

    @staticmethod
    def get_by_email(email):
        try:
            user = CustomUser.objects.get(id=email)
        except CustomUser.DoesNotExist:
            raise Exception("User does not exist.")
        else:
            return user

    @staticmethod
    def delete_by_id(user_id):
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
        users = CustomUser.objects.all()
        return users

    def get_role_name(self):
        if self.role:
            return 'staff'
        else:
            return 'user'

    def get_absolute_url(self):
        return reverse('user_by_id', kwargs={'id': self.id})
