# Generated by Django 5.0.2 on 2024-02-26 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_contactmessage_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='created_at',
            field=models.TimeField(auto_now=True),
        ),
    ]
