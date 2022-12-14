import django
from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from datetime import datetime


class my_account_manager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class account(AbstractBaseUser):
    # 320 Characters is the max len of a email.
    email = models.EmailField(max_length=320, unique=True, primary_key=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)

    USERNAME_FIELD = 'email'

    objects = my_account_manager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class faculty(models.Model):

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say')
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emp_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    school = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER)
    phone = models.IntegerField()

    def __str__(self):
        return str(self.emp_id)


class administrator(models.Model):

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say')
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    admin_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER)
    phone = models.IntegerField()

    def __str__(self):
        return str(self.emp_id)


class course(models.Model):

    course_code = models.CharField(max_length=10, primary_key=True)
    course_name = models.CharField(max_length=64)

    lecture_hours = models.IntegerField()
    tutorial_hours = models.IntegerField()
    practical_hours = models.IntegerField()
    j_project_hours = models.IntegerField()

    credits = models.IntegerField()

    def __str__(self):
        return str(self.course_code)


class preference(models.Model):
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emp_id = models.IntegerField(primary_key=True)
    preferences = models.ManyToManyField(course)
