# Generated by Django 5.0 on 2024-04-15 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrationindexpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='bureauxindexpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='commissionsindexpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='conferencesindexpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='conseilsindexpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
    ]
