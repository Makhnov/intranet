# Generated by Django 5.0 on 2024-04-15 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amicale', '0004_amicaleinscriptionpage_introduction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amicaleindexpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='amicaleinscriptionpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
    ]
