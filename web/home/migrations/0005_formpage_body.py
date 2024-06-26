# Generated by Django 5.0 on 2024-04-15 06:31

import utils.streamfield
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_advancedformsetting_to_subject_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('media', utils.streamfield.CustomMediaBlock(icon='media')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(help_text='Enter the URL.', label='URL')), ('text', wagtail.blocks.CharBlock(help_text='Enter the visible text for this link (optional).', label='Replacement Text', required=False))], icon='link')), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.embeds.blocks.EmbedBlock(label='URL a intégrer')), ('resolution', wagtail.blocks.ChoiceBlock(choices=[('very_small', 'Very small'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('very_large', 'Very large')], label='Size of the frame')), ('alternative_title', wagtail.blocks.CharBlock(blank=True, help_text='Alternative title for users accessibility.', label='Alternative title', required=False))], icon='media')), ('list', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(icon='radio-full'), icon='list-ul')), ('quote', wagtail.blocks.BlockQuoteBlock(icon='openquote'))], blank=True, help_text='This is the main content of the page.', null=True, verbose_name='Agenda'),
        ),
    ]
