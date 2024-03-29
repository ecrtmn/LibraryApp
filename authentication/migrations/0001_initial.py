# Generated by Django 3.1.1 on 2020-12-25 16:40

import authentication.models
import authentication.utils
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(max_length=100, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('password', models.CharField(max_length=128, validators=[authentication.utils.validate_password])),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('role', models.IntegerField(choices=[(0, 'user'), (1, 'staff')], default=0)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', authentication.models.CustomUserManager()),
            ],
        ),
    ]
