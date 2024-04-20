# Generated by Django 5.0.4 on 2024-04-20 08:01

import utils.streamfield
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_alter_administrationindexpage_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compterendupage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title', icon='title', label='Heading')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow', label='Paragraph')), ('media', utils.streamfield.CustomMediaBlock(icon='media', label='Media')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', label='Image')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full', label='Document')), ('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(help_text='Enter the URL.', label='URL')), ('text', wagtail.blocks.CharBlock(help_text='Enter the visible text for this link (optional).', label='Replacement Text', required=False))], icon='link', label='Link')), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.embeds.blocks.EmbedBlock(label='URL a intégrer')), ('resolution', wagtail.blocks.ChoiceBlock(choices=[('very_small', 'Very small'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('very_large', 'Very large')], label='Size of the frame')), ('alternative_title', wagtail.blocks.CharBlock(blank=True, help_text='Alternative title for users accessibility.', label='Alternative title', required=False))], icon='media', label='Embed media')), ('list', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(icon='list-ul', label='List Item'), icon='list-ul', label='List')), ('quote', wagtail.blocks.BlockQuoteBlock(icon='openquote', label='Quote')), ('table', wagtail.contrib.table_block.blocks.TableBlock(icon='table', label='Table', table_options={'autoColumnSize': False, 'colHeaders': True, 'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo', '---------', 'copy', 'cut', '---------', 'alignment', '---------', 'mergeCells'], 'height': 108, 'language': 'fr-FR', 'mergeCells': True, 'minSpareRows': 0, 'renderer': 'text', 'rowHeaders': True, 'startCols': 3, 'startRows': 3})), ('PDF', wagtail.blocks.StructBlock([('pdf_document', wagtail.documents.blocks.DocumentChooserBlock(help_text='Chose a PDF wich will be converted to images and added in the flow. Name smartly the document, it will be used to create a collection.', label='Document', required=True)), ('pdf_import', wagtail.blocks.BooleanBlock(default=False, help_text='Use cautiously. It will override all existing images in this section.', label='Save and import', required=False)), ('pdf_images', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(required=False), form_classname='collapsible, collapsed', help_text='You can remove or replace any of the images below. If you want to restore the original images, click again on the import button.', label='Aperçu des pages', required=False))], icon='doc-full', label='PDF')), ('DOCX', wagtail.blocks.StructBlock([('docx_document', wagtail.documents.blocks.DocumentChooserBlock(help_text='Chose a DOCX file to import in the flow.', label='Document', required=True)), ('docx_import', wagtail.blocks.BooleanBlock(default=False, help_text='Use cautiously. It will override all existing content in this section.', label='Save and import', required=False)), ('docx_content', wagtail.blocks.StreamBlock([('heading', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(label='content', required=True)), ('heading_level', wagtail.blocks.ChoiceBlock(choices=[('h1', 'Heading 1'), ('h2', 'Heading 2'), ('h3', 'Heading 3'), ('h4', 'Heading 4'), ('h5', 'Heading 5'), ('h6', 'Heading 6')], label='level', required=False)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False))])), ('paragraph', wagtail.blocks.StructBlock([('paragraph', wagtail.blocks.RichTextBlock(label='content', required=True)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False))])), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='content', required=True)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('icon', 'Icon'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('full', 'Full')], required=False))])), ('table', wagtail.blocks.StructBlock([('table', wagtail.contrib.table_block.blocks.TableBlock(label='content', required=True, table_options={'autoColumnSize': False, 'colHeaders': True, 'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo', '---------', 'copy', 'cut', '---------', 'alignment', '---------', 'mergeCells'], 'height': 108, 'language': 'fr-FR', 'mergeCells': True, 'minSpareRows': 0, 'renderer': 'text', 'rowHeaders': True, 'startCols': 3, 'startRows': 3})), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False))]))], classname='collapsible, collapsed', help_text='You can remove or replace any of the content below. If you want to restore the original content, click again on the import button.', label='Aperçu du contenu', required=False))], icon='doc-full', label='DOCX'))], blank=True, help_text='This is the main content of the page.', null=True, verbose_name='Main review'),
        ),
    ]
