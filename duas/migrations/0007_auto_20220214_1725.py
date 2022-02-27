# Generated by Django 2.2.5 on 2022-02-14 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('duas', '0006_auto_20220214_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuaCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=300, verbose_name='Category')),
            ],
            options={
                'verbose_name_plural': 'DuaCategory',
            },
        ),
        migrations.AddField(
            model_name='duas',
            name='reference',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='duas',
            name='zekr',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Zekar'),
        ),
        migrations.AlterField(
            model_name='duas',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='duas', to='duas.DuaCategory', verbose_name='Category'),
        ),
        migrations.DeleteModel(
            name='DuasData',
        ),
    ]
