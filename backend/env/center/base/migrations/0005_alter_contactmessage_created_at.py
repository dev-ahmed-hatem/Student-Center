# Generated by Django 5.0.2 on 2024-02-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_contactmessage_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='created_at',
            field=models.TimeField(verbose_name='created at'),
        ),
    ]
