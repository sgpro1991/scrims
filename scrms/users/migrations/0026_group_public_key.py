# Generated by Django 2.0.1 on 2018-02-20 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_message_reading_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='public_key',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]