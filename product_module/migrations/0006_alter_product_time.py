# Generated by Django 5.1.3 on 2024-12-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0005_alter_product_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='time',
            field=models.IntegerField(default=1, verbose_name='زمان آموزش'),
        ),
    ]
