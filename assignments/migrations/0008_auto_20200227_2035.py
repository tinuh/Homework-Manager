# Generated by Django 2.2.5 on 2020-02-28 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0007_auto_20200227_2024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='linked_model_class',
            new_name='linked_model_assignment',
        ),
    ]
