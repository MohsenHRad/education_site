# Generated by Django 5.1.3 on 2024-12-05 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0007_productcategory_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
    ]