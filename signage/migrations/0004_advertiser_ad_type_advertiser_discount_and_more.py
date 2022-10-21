# Generated by Django 4.1.1 on 2022-10-03 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0003_advertiser_businesses'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertiser',
            name='ad_type',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='advertiser',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advertiser',
            name='length_of_ad',
            field=models.IntegerField(default=0),
        ),
    ]
