# Generated by Django 5.1.3 on 2024-12-03 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0004_alter_product_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='time',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='زمان آموزش'),
        ),
    ]