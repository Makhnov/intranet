# Generated by Django 5.0.4 on 2024-04-20 16:04

import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailmedia.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amicale', '0009_alter_amicalepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amicalepage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title', icon='title', label='Heading')), ('paragraph', wagtail.blocks.StructBlock([('paragraph', wagtail.blocks.RichTextBlock(label='content', required=True)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False))], icon='pilcrow', label='Paragraph')), ('media', wagtail.blocks.StructBlock([('media', wagtailmedia.blocks.AbstractMediaChooserBlock(help_text='Choose a media item', required=True)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('very_small', 'Very small'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('very_large', 'Very large')], label='Size of the frame')), ('alternative_title', wagtail.blocks.CharBlock(blank=True, help_text='Alternative title for users accessibility.', label='Alternative title', required=False))], icon='media', label='Media')), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='content', required=True)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('icon', 'Icon'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('full', 'Full')], required=False))], icon='image', label='Image')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse', label='Document')), ('table', wagtail.blocks.StructBlock([('table', wagtail.contrib.table_block.blocks.TableBlock(label='content', required=True, table_options={'autoColumnSize': False, 'colHeaders': True, 'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo', '---------', 'copy', 'cut', '---------', 'alignment', '---------', 'mergeCells'], 'height': 108, 'language': 'fr-FR', 'mergeCells': True, 'minSpareRows': 0, 'renderer': 'text', 'rowHeaders': True, 'startCols': 3, 'startRows': 3})), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('icon', 'Icon'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('full', 'Full')], required=False))], icon='table', label='Table')), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.embeds.blocks.EmbedBlock(label='URL a intégrer')), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('icon', 'Icon'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('full', 'Full')], required=False)), ('alternative_title', wagtail.blocks.CharBlock(blank=True, help_text='Alternative title for users accessibility.', label='Alternative title', required=False))], icon='media', label='Embed media')), ('list', wagtail.blocks.StructBlock([('list', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(icon='radio-full', label='Item', required=True), icon='list-ul', label='List')), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('icon', 'Icon'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('full', 'Full')], required=False))], icon='list-ul', label='List')), ('quote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.BlockQuoteBlock(label='Quote', required=True)), ('author', wagtail.blocks.CharBlock(label='Author', required=False)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('icon', 'Icon'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('full', 'Full')], required=False))], icon='openquote', label='Quote'))], blank=True, help_text='This is the main content of the page.', null=True, verbose_name='Agenda'),
        ),
    ]