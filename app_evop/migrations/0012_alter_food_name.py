# Generated by Django 4.2.4 on 2023-09-15 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_evop', '0011_alter_food_be_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='name',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
    ]