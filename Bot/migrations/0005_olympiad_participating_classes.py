# Generated by Django 3.2.6 on 2021-08-27 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0004_olympiad'),
    ]

    operations = [
        migrations.AddField(
            model_name='olympiad',
            name='participating_classes',
            field=models.ManyToManyField(to='Bot.Class'),
        ),
    ]
