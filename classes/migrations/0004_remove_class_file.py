# Generated by Django 2.2.6 on 2019-10-26 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_class_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='file',
        ),
    ]
