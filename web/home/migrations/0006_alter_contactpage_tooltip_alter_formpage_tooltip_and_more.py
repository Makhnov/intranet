# Generated by Django 5.0 on 2024-04-15 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_formpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='genericpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='instantdownloadpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='publicpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
        migrations.AlterField(
            model_name='ressourcespage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
    ]
