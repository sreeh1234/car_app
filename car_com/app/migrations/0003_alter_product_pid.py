# Generated by Django 5.1.4 on 2025-01-03 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.TextField(unique=True),
        ),
    ]
