# Generated by Django 4.1.1 on 2022-11-11 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0006_pabblysubscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertiser',
            name='ad_type',
        ),
        migrations.RemoveField(
            model_name='advertiser',
            name='discount',
        ),
    ]
