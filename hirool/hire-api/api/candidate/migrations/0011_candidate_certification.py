# Generated by Django 2.0.6 on 2020-01-22 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0010_auto_20200122_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='certification',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
