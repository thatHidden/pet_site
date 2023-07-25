import random
import string

from django.contrib import auth
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django_project import settings


class CustomUser(AbstractUser):
    """Extends default User model (I hope I did it right(anyway it works))"""
    photo = models.ImageField(upload_to="user_photo/%Y/%m/%d/", verbose_name="Photo", blank=True, null=True,
                              default="user_photo/default.png")
    bookmarks = models.ManyToManyField('axaxa.Cars', related_name='bookmarked_by', blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_set",
        related_query_name="user",
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )


class AvailableCarList(models.Model):
    brand = models.CharField(max_length=25, null=False)
    model = models.CharField(max_length=50, null=False)
    generation = models.IntegerField(null=False)
    body = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.brand})


class Cars(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=1, related_name="lots")
    brand = models.CharField(max_length=25, null=False)
    model = models.CharField(max_length=50, null=False)
    generation = models.CharField(max_length=10, null=False)
    body = models.CharField(max_length=20, null=False)
    description = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(null=False)
    start_price = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    bid = models.IntegerField(null=True)
    bid_holder = models.ForeignKey('axaxa.CustomUser', on_delete=models.PROTECT, null=True, related_name="bids")
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", null=True)
    slug = models.SlugField(max_length=255, unique=False, db_index=True, verbose_name="URL")

    class Meta:
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.brand


class Comment(models.Model):
    post = models.ForeignKey(Cars, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_create']


class Reply(Comment):
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE)


class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    lot = models.ForeignKey(Cars, on_delete=models.PROTECT, related_name='bids')
    price = models.IntegerField(validators=[MinValueValidator(0)])
    time = models.DateTimeField(auto_now_add=True)
