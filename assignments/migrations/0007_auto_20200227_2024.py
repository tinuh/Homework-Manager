# Generated by Django 2.2.5 on 2020-02-28 01:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_class_linker'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignments', '0006_auto_20200227_2022'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Model_class',
            new_name='Model_assignment',
        ),
    ]
