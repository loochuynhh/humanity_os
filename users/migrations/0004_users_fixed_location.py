# Generated by Django 5.1.7 on 2025-04-14 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_checkincheckout_checkin_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='fixed_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
