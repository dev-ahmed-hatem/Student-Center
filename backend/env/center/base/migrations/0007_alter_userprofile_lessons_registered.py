# Generated by Django 5.0.2 on 2024-05-02 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_userprofile_lessons_registered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='lessons_registered',
            field=models.ManyToManyField(blank=True, to='base.lesson', verbose_name='Lessons Registered'),
        ),
    ]
