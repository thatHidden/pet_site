# Generated by Django 4.2 on 2023-07-25 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axaxa', '0002_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
