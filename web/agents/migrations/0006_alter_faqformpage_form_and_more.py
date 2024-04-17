# Generated by Django 5.0.4 on 2024-04-17 03:25

import wagtail.blocks
import wagtail.fields
import wagtailstreamforms.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_alter_faqindexpage_tooltip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqformpage',
            name='form',
            field=wagtail.fields.StreamField([('form_field', wagtail.blocks.StructBlock([('form', wagtailstreamforms.blocks.FormChooserBlock()), ('form_action', wagtail.blocks.CharBlock(help_text='The form post action. "" or "." for the current page or a url', required=False)), ('form_reference', wagtailstreamforms.blocks.InfoBlock(help_text='This form will be given a unique reference once saved', required=False))], icon='form', label='Form field'))], blank=True, help_text='The main form for the inscription to the amicale.', null=True, verbose_name='Inscription form'),
        ),
        migrations.AlterField(
            model_name='faqformpage',
            name='introduction',
            field=wagtail.fields.RichTextField(blank=True, help_text='Here you can explain how the inscription works...', null=True, verbose_name='Introduction'),
        ),
        migrations.AlterField(
            model_name='faqformpage',
            name='tooltip',
            field=models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip.'),
        ),
    ]