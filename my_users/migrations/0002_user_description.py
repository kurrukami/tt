# Generated by Django 3.1.2 on 2020-11-04 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
