from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    company_name = models.CharField(max_length=120)
    personal_telephone = models.CharField(max_length=16)
    office_telephone = models.CharField(max_length=16)
    address = models.TextField(max_length=250)
    last_login = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


TYPES = (
    ("Energy (Renewable & Non-renewable)", "Energy (Renewable & Non-renewable)"),
    ("Manufacturing", "Manufacturing"),
    ("Transportation", "Transportation"),
    ("Agriculture & Food Production", "Agriculture & Food Production"),
    ("Construction & Real Estate", "Construction & Real Estate"),
    ("Financial Services", "Financial Services"),
    ("Technology & Telecommunications", "Technology & Telecommunications"),
    ("Healthcare & Pharmaceuticals", "Healthcare & Pharmaceuticals"),
    ("Hospitality & Tourism", "Hospitality & Tourism"),
    ("Retail & Consumer Goods", "Retail & Consumer Goods"),
    ("Utilities", "Utilities"),
    ("Government & Public Sector", "Government & Public Sector"),
    ("Education", "Education"),
    ("Entertainment & Media", "Entertainment & Media"),
    ("Non-profit & NGO", "Non-profit & NGO"),
    ("Other", "Other"),
)

REASONS = (
    ("Know my carbon footprints", "Know my carbon footprints"),
    ("Generate a sustainability report", "Generate a sustainability report"),
    ("Go through the application", "Go through the application"),
    ("Request a Demo", "Request a Demo")
)


class Category(models.Model):
    reason = models.CharField(max_length=55, null=True, blank=True, choices=REASONS)
    type = models.CharField(max_length=55, null=True, blank=True, choices=TYPES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
