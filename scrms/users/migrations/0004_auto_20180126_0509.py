# Generated by Django 2.0.1 on 2018-01-26 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180125_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type_msg',
            field=models.CharField(choices=[(0, 'text'), (1, 'img'), (2, 'file'), (3, 'link')], default=False, max_length=255),
        ),
    ]