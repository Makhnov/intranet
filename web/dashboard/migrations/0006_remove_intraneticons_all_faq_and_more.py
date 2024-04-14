# Generated by Django 5.0 on 2024-04-12 03:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_intraneticons_star'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intraneticons',
            name='all_faq',
        ),
        migrations.AddField(
            model_name='intraneticons',
            name='amicale_all',
            field=models.ForeignKey(blank=True, help_text='All Amicale pages', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Amicale all'),
        ),
        migrations.AddField(
            model_name='intraneticons',
            name='faq_all',
            field=models.ForeignKey(blank=True, help_text='All FAQ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='All FAQ'),
        ),
    ]