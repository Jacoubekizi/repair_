# Generated by Django 5.0.6 on 2024-05-11 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='name',
        ),
    ]
