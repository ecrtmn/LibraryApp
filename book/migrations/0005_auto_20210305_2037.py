# Generated by Django 3.1.1 on 2021-03-05 18:37

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20201225_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
