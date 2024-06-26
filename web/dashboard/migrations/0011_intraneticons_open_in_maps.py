# Generated by Django 5.0.4 on 2024-04-18 05:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_intraneticons_inscription'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='intraneticons',
            name='open_in_maps',
            field=models.ForeignKey(blank=True, help_text='Open in maps icon', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Open in maps'),
        ),
    ]
