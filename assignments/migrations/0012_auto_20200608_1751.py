# Generated by Django 3.0.7 on 2020-06-08 21:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0011_assignment_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='model_assignment',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]