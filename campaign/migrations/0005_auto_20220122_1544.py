# Generated by Django 2.2.5 on 2022-01-22 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0004_auto_20220122_1224'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Campaign',
            new_name='MosqueCampaign',
        ),
        migrations.CreateModel(
            name='DonationArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField()),
                ('mosque_compaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donation_areas', to='campaign.MosqueCampaign')),
            ],
            options={
                'verbose_name_plural': 'Donation Areas',
                'ordering': ['-created_on'],
            },
        ),
    ]
