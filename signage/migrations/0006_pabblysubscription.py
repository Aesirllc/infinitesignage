# Generated by Django 4.1.1 on 2022-10-13 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0005_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='PabblySubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_id', models.CharField(max_length=150)),
                ('customer_id', models.CharField(max_length=150)),
                ('advertiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='signage.advertiser')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='signage.plan')),
            ],
        ),
    ]
