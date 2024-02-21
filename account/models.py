# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier for authentication instead of usernames.
    
    Inherits methods from BaseUserManager and overrides the default behavior for creating users and superusers.
    
    Methods:
        create_user(self, email, password=None, **extra_fields):
            Creates and saves a regular user with the given email and password.

        create_superuser(self, email, password=None, **extra_fields):
            Creates and saves a superuser with the given email, password, and superuser privileges.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email, password, and superuser privileges.
        """
            
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user account.

    This class extends the AbstractBaseUser and PermissionsMixin classes provided by Django,
    allowing for custom user authentication and permissions management.
    """

    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
