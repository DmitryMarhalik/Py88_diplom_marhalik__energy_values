# Generated by Django 4.2.4 on 2023-08-16 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_evop', '0004_alter_food_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='carbohydrates',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='fats',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='proteins',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
    ]
