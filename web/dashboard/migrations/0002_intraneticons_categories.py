# Generated by Django 5.0 on 2024-04-08 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='intraneticons',
            name='categories',
            field=models.ForeignKey(blank=True, help_text='Related theme icon for numerous pages', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Themes'),
        ),
    ]
