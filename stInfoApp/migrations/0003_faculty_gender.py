# Generated by Django 3.2.7 on 2021-12-01 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stInfoApp', '0002_auto_20211029_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='Gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female')], default='default', max_length=15),
            preserve_default=False,
        ),
    ]
