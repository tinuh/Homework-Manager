# Generated by Django 2.2.6 on 2019-10-26 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '0005_auto_20191026_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='class_linker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.Class')),
                ('linked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
