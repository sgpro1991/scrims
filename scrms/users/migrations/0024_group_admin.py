# Generated by Django 2.0.1 on 2018-02-20 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20180216_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='admin',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]