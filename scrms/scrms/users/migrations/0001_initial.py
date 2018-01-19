# Generated by Django 2.0.1 on 2018-01-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='user/', verbose_name='')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('subordinate', models.TextField(blank=True)),
                ('about', models.TextField(blank=True)),
            ],
        ),
    ]
