from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    brand = models.CharField(max_length=25, null=False)
    model = models.CharField(max_length=50, null=False)
    generation = models.CharField(max_length=10, null=False)
    body = models.CharField(max_length=20, null=False)
    description = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(null=False)
    start_price = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    bid = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", null=True)
    slug = models.SlugField(max_length=255, unique=False, db_index=True, verbose_name="URL")

    class Meta:
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.brand

    def save(self, *args, **kwargs):
        self.bid = self.start_price
        super(Cars, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Cars, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_create']


class Reply(Comment):
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE)




