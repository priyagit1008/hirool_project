# Generated by Django 2.0.6 on 2020-06-17 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20200616_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, max_length=255, upload_to=''),
        ),
    ]
