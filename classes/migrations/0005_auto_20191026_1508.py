# Generated by Django 2.2.6 on 2019-10-26 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_remove_class_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='user',
            new_name='teacher',
        ),
        migrations.AddField(
            model_name='class',
            name='code',
            field=models.CharField(default='QG9JU3', max_length=6),
            preserve_default=False,
        ),
    ]
