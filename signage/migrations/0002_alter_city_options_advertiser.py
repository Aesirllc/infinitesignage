# Generated by Django 4.1.1 on 2022-10-03 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'cities'},
        ),
        migrations.CreateModel(
            name='Advertiser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('contact_name', models.CharField(max_length=50)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('address', models.TextField()),
                ('salesman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
