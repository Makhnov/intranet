# Generated by Django 5.0 on 2024-04-12 01:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_intraneticons_spinner'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='intraneticons',
            name='star',
            field=models.ForeignKey(blank=True, help_text='New informations added in the last 14 days', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Star'),
        ),
    ]
