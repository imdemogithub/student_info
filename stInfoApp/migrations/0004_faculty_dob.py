# Generated by Django 3.2.7 on 2021-12-01 09:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stInfoApp', '0003_faculty_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='DoB',
            field=models.DateField(auto_created=True, default=django.utils.timezone.now),
        ),
    ]