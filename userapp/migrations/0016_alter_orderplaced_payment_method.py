# Generated by Django 5.0.2 on 2024-04-17 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0015_alter_orderplaced_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='payment_method',
            field=models.CharField(max_length=20),
        ),
    ]
