# Generated by Django 4.1.1 on 2022-12-16 16:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0008_pabblysubscription_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
