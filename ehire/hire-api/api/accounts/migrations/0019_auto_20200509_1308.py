# Generated by Django 2.0.6 on 2020-05-09 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20200507_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image_url',
            field=models.ImageField(max_length=255, upload_to=''),
        ),
    ]
