# Generated by Django 5.0 on 2024-04-12 05:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_remove_intraneticons_all_faq_and_more'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='intraneticons',
            name='home_all',
            field=models.ForeignKey(blank=True, help_text='All cloud pages', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Home all'),
        ),
        migrations.AddField(
            model_name='intraneticons',
            name='home_none',
            field=models.ForeignKey(blank=True, help_text='Home unknown page type', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Home unknown'),
        ),
    ]
