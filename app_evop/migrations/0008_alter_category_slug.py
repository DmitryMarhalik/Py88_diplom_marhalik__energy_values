# Generated by Django 4.2.4 on 2023-08-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_evop', '0007_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='URL category'),
        ),
    ]