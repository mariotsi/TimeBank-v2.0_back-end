from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class City(models.Model):
    name = models.CharField(max_length=200)
    province = models.CharField(max_length=2)
    region = models.CharField(max_length=3)
    area_code = models.CharField(max_length=6)
    cap = models.CharField(max_length=5)
    cadastral_code = models.CharField(max_length=4)
    inhabitants = models.BigIntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, username, address, city, password=None, ):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            city=city,
            address=address,


        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username, address, city=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not city:
            city = City(
                name="FakeName",
                province="ZZ",
                region="FakeRegion",
                area_code="Fake",
                cap="00000",
                cadastral_code=99999,
                inhabitants=1
            )
            city.save()

        user = self.create_user(email,
                                password=password,
                                username=username,
                                address=address,
                                city=city,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=40,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    available_hours = models.IntegerField(default=0)
    worked_hours = models.IntegerField(default=0)
    requested_hours = models.IntegerField(default=0)
    used_hours = models.IntegerField(default=0)
    address = models.TextField(default="Home")
    city = models.ForeignKey(City)

    class Meta:
        ordering = ['username']
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'address']

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):
        return self.username + " " + self.email + " " + self.city.cap + " " \
               + str(self.city.name) + " (" + self.city.province + ") - is admin:" + str(self.is_staff)

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


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['category_id']

    def __str__(self):
        return self.name


class Listing(models.Model):
    creation_date = models.DateField()
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category)
    owner = models.ForeignKey(User, related_name='listing_owned')
    applicant = models.ForeignKey(User, default=None, null=True, blank=True, related_name='listing_requested')
    requested = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        if self.requested:
            return self.description[:30] + ". Owner: " + str(
                self.owner.username) + ". Category: " + self.category.name + ". Applicant: " + str(
                self.applicant.username) + " " + str(self.creation_date) + " is requested: " + str(self.requested)
        else:
            return self.description[:30] + ". Owner: " + str(
                self.owner.username) + ". Category: " + self.category.name + ". " + str(
                self.creation_date) + " is requested: " + str(self.requested)