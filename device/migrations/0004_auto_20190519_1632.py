# Generated by Django 2.1 on 2019-05-19 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_device_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='number',
            field=models.TextField(unique=True),
        ),
    ]
