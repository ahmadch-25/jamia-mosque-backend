# Generated by Django 2.2.5 on 2022-04-14 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paryertiming', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prayertiming',
            name='asr',
        ),
        migrations.RemoveField(
            model_name='prayertiming',
            name='dhuhr',
        ),
        migrations.RemoveField(
            model_name='prayertiming',
            name='fajr',
        ),
        migrations.RemoveField(
            model_name='prayertiming',
            name='isha',
        ),
        migrations.RemoveField(
            model_name='prayertiming',
            name='maghrib',
        ),
    ]
