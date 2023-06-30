import string, random

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


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
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name="lots")
    brand = models.CharField(max_length=25, null=False)
    model = models.CharField(max_length=50, null=False)
    generation = models.CharField(max_length=10, null=False)
    body = models.CharField(max_length=20, null=False)
    description = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(null=False)
    start_price = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    bid = models.IntegerField(null=True)
    bid_holder = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="bids")
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
        while True:
            characters = string.ascii_uppercase + string.digits
            random_string = ''.join(random.choice(characters) for _ in range(4))
            self.slug = random_string + "-" + slugify(self.brand + "-" +
                                                self.model + "-" +
                                                      (self.generation if self.generation != "1" else ""))
            if not Cars.objects.filter(slug=self.slug).exists():
                break
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




