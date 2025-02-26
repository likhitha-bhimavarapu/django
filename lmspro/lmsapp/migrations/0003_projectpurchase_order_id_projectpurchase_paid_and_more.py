# Generated by Django 5.1.2 on 2024-11-08 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0002_projectpurchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpurchase',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='projectpurchase',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projectpurchase',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
