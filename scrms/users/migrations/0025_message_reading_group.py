# Generated by Django 2.0.1 on 2018-02-20 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_group_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reading_group',
            field=models.ManyToManyField(blank=True, to='users.User'),
        ),
    ]