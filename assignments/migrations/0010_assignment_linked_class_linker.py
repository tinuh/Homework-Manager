# Generated by Django 2.2.5 on 2020-03-18 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_class_linker'),
        ('assignments', '0009_auto_20200227_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='linked_class_linker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.class_linker'),
        ),
    ]
