# Generated by Django 2.0.6 on 2020-02-25 18:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20200225_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissions',
            name='permissions',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, choices=[('candidate_add', 'True'), ('candidate_edit', 'False'), ('candidate_read', 'false')], max_length=256, null=True),
        ),
    ]