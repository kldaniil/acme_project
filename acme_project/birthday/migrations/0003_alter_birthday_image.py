# Generated by Django 3.2.16 on 2025-01-16 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthday', '0002_auto_20250116_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthday',
            name='image',
            field=models.ImageField(blank=True, upload_to='birthdays_images', verbose_name='Фото'),
        ),
    ]
