# Generated by Django 5.0.2 on 2024-03-27 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0006_remove_orderplaced_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('image', models.ImageField(upload_to='user-images/')),
            ],
        ),
    ]
