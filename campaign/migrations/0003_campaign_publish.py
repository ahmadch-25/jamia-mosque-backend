# Generated by Django 2.2.5 on 2022-01-22 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_auto_20220122_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='publish',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
