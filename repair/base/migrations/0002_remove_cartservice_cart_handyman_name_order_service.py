# Generated by Django 5.0.6 on 2024-05-10 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartservice',
            name='cart',
        ),
        migrations.AddField(
            model_name='handyman',
            name='name',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ManyToManyField(to='base.service'),
        ),
    ]
