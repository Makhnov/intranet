# Generated by Django 5.0 on 2024-04-15 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_alter_faqformpage_options_remove_faqformpage_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqformpage',
            name='date_from',
            field=models.DateField(blank=True, help_text='Start date of the survey.', null=True, verbose_name='From'),
        ),
        migrations.AddField(
            model_name='faqformpage',
            name='date_to',
            field=models.DateField(blank=True, help_text='End date of the survey.', null=True, verbose_name='To'),
        ),
    ]