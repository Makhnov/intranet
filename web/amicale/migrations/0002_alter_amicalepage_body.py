# Generated by Django 5.0 on 2024-03-29 19:44

import utils.streamfield
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amicale', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amicalepage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title', icon='title', label='Heading')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow', label='Paragraph')), ('media', utils.streamfield.CustomMediaBlock(icon='media', label='Media')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', label='Image')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', label='Document')), ('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(help_text='Enter the URL.', label='URL')), ('text', wagtail.blocks.CharBlock(help_text='Enter the visible text for this link (optional).', label='Replacement Text', required=False))], icon='link', label='Link')), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.embeds.blocks.EmbedBlock(label='URL a intégrer')), ('resolution', wagtail.blocks.ChoiceBlock(choices=[('very_small', 'Very small'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('very_large', 'Very large')], label='Size of the frame')), ('alternative_title', wagtail.blocks.CharBlock(blank=True, help_text='Alternative title for users accessibility.', label='Alternative title', required=False))], icon='media', label='Embed media')), ('list', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(icon='radio-full', label='Item'), icon='list-ul', label='List')), ('quote', wagtail.blocks.BlockQuoteBlock(icon='openquote', label='Quote'))], blank=True, help_text='This is the main content of the page.', null=True, verbose_name='Agenda'),
        ),
    ]
