# Generated by Django 4.2 on 2023-08-03 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axaxa', '0004_alter_customuser_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='photo',
            field=models.ImageField(default='photos/default.png', null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
