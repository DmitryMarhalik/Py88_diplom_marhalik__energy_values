# Generated by Django 4.2.4 on 2023-08-22 00:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_evop', '0009_alter_category_options_alter_intake_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intake',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
