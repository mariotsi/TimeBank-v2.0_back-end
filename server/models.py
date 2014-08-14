from django.db import models
import json
import os


# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['category_id']

    def __str__(self):
        return self.name


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
        return str(self.name)


class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField('password', max_length=128, help_text=(
        "At least 8 character"))
    email = models.EmailField(unique=True)
    available_hours = models.IntegerField(default=0)
    worked_hours = models.IntegerField(default=0)
    requested_hours = models.IntegerField(default=0)
    used_hours = models.IntegerField(default=0)
    address = models.TextField()
    city = models.ForeignKey(City)
    admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username + " " + self.email + " " + self.city.cap + " " \
            + str(self.city.name) + " (" + self.city.province + ") - is admin:" + str(self.admin)


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
