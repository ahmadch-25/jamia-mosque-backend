# Generated by Django 2.2.5 on 2022-01-29 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone Number'),
        ),
    ]
