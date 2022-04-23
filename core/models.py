import os

from django.db.models import Max
from rest_framework.authtoken.models import Token

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Tier(models.Model):
    """
    Tier model
    """
    tier_name = models.CharField(
        max_length=200,
        verbose_name="Nom du client",
        help_text="Entrez le nom de votre client")
    address = models.CharField(
        max_length=200,
        verbose_name="Adresse du client",
        help_text="Entrez l'adresse de votre client")
    email = models.EmailField()
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.tier_name


class Role(models.Model):
    """
    Role model
    """
    role_name = models.CharField(
        max_length=200,
        verbose_name="Role du contact",
        help_text="Entrez le role de votre contact")

    def __str__(self):
        return self.role_name


class Contact(models.Model):
    """
    Contacts model
    """
    contact_name = models.CharField(
        max_length=200,
        verbose_name="Nom du contact",
        help_text="Entrez le nom de votre contact")
    # contact_last_name = models.CharField(
    #     max_length=200,
    #     verbose_name="Prénom du contact",
    #     help_text="Entrez le prénom de votre contact")
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Numéro de téléphone",
        help_text="Entrez le numéro de téléphone")
    id_tier = models.ForeignKey(
        Tier,
        on_delete=models.CASCADE,
        verbose_name="Nom du client",
        help_text="Affectez le contact à votre client")
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Nom de l'opérateur",
        help_text="Affectez le contact à un opérateur")

    id_role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name="Role du contact",
        help_text="Affectez le role du contact")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.contact_name


class CallLog(models.Model):
    """
    Call log model
    """
    id_user = models.CharField(
        max_length=50, )
    call_type = models.CharField(
        max_length=50)
    id_call = models.CharField(
        max_length=50)
    call_started_at = models.CharField(
        max_length=50)
    duration = models.CharField(
        max_length=50)
    id_log = models.CharField(
        max_length=200)
    called_phone_number = models.CharField(
        max_length=20)
    position_call_log = models.CharField(
        max_length=50)
    id_device = models.CharField(
        max_length=50)
    reception_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.called_phone_number + "-" + self.call_type

    @staticmethod
    def get_max_position(self, my_id_device):
        max_position_call_log = CallLog.objects.aggregate(Max('position_call_log'))['position_call_log__max']
        # max_position_call_log = CallLog.objects.filter(id_device=my_id_device).annotate(
        #     position_call_log=Max('position_call_log'))
        # .aggregate(Max('position_call_log'))['position_call_log__max']
        # print(max_position_call_log, os.getcwd())
        return max_position_call_log

    @staticmethod
    def get_id_device(self):
        id_device = CallLog.objects.values('id_device')
        return id_device

    def save(self, *args, **kwargs):
        super(CallLog, self).save(*args, **kwargs)
        if not Position.objects.all():
            Position(id_device=self.get_id_device(self),
                     max_position_call_log=self.get_max_position(self, self.get_id_device(self))).save()
        else:
            Position.objects.filter(id_device=self.get_id_device(self)).update(id_device=self.get_id_device(self),
                                                                               max_position_call_log=self.get_max_position(
                                                                                   self, self.get_id_device(self)))
            # max_id = Position.max_id()
            # Position.objects.filter(id=max_id).update(id_log=1,
            # max_position_call_log = self.get_max_position(self))


class Position(models.Model):
    """
    Transaction model
    """
    id_device = models.CharField(
        max_length=200)
    max_position_call_log = models.IntegerField(max_length=20)
    reception_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_device

    @staticmethod
    def max_id():
        max_id = Position.objects.values('id').order_by('-id').first()['id']
        return max_id


class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, password, **other_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True'))

        return self.create_user(email, user_name, first_name, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
    )
    user_name = models.CharField(_('username'), max_length=150, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    about = models.CharField(_('about'), max_length=500, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']  # Email & Password are required by default.

    def __str__(self):
        return self.user_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
