# Generated by Django 5.0.6 on 2024-07-18 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_remove_booking_user_booking_age_booking_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='firstname',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='booking',
            name='lastname',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='booking',
            name='number_of_tickets',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='phonenumber',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='booking',
            name='wilaya',
            field=models.CharField(max_length=100),
        ),
    ]