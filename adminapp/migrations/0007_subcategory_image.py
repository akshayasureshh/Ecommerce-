# Generated by Django 5.0.2 on 2024-04-06 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_croppedimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(null=True, upload_to='subcate_image'),
        ),
    ]
