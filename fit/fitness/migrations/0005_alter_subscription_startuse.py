# Generated by Django 3.2.6 on 2021-08-10 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0004_remove_subscription_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='startUse',
            field=models.DateField(blank=True, verbose_name='Начало пользования'),
        ),
    ]