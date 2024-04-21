# Generated by Django 5.0.4 on 2024-04-21 08:23

import utils.faq
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
        ('agents', '0008_alter_faqpage_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqpage',
            name='answer',
            field=wagtail.fields.StreamField([('single_answer', wagtail.blocks.StreamBlock([('heading', wagtail.blocks.CharBlock(form_classname='title', icon='title', label='Heading')), ('paragraph', wagtail.blocks.RichTextBlock(editor='full', icon='pilcrow', label='Paragraph')), ('media', wagtail.blocks.StructBlock([('media', wagtailmedia.blocks.AbstractMediaChooserBlock(help_text='Choose a media item', required=True)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('very_small', 'Very small'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('very_large', 'Very large')], label='Size of the frame')), ('alternative_title', wagtail.blocks.CharBlock(blank=True, help_text='Alternative title for users accessibility.', label='Alternative title', required=False))], icon='media', label='Media')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', label='Image')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full', label='Document')), ('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(help_text='Enter the URL.', label='URL')), ('text', wagtail.blocks.CharBlock(help_text='Enter the visible text for this link (optional).', label='Replacement Text', required=False))], icon='link', label='Link')), ('button', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(help_text='Enter the URL.', label='URL', required=True)), ('text', wagtail.blocks.CharBlock(help_text='Enter the visible text for this link (optional).', label='Button text', required=False)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('icon', wagtail.images.blocks.ImageChooserBlock(help_text='Optionnal', icon='image', label='Button image', required=False))], icon='button', label='Button')), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.embeds.blocks.EmbedBlock(label='URL a intégrer')), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('icon', 'Icon'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('full', 'Full')], required=False)), ('alternative_title', wagtail.blocks.CharBlock(blank=True, help_text='Alternative title for users accessibility.', label='Alternative title', required=False))], icon='media', label='Embed')), ('list', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(icon='list-ul', label='List Item'), icon='list-ul', label='List')), ('quote', wagtail.blocks.BlockQuoteBlock(icon='openquote', label='Quote')), ('table', wagtail.contrib.table_block.blocks.TableBlock(icon='table', label='Table', table_options={'autoColumnSize': False, 'colHeaders': True, 'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo', '---------', 'copy', 'cut', '---------', 'alignment', '---------', 'mergeCells'], 'height': 108, 'language': 'fr-FR', 'mergeCells': True, 'minSpareRows': 0, 'renderer': 'text', 'rowHeaders': True, 'startCols': 3, 'startRows': 3}))], icon='doc-full', label='Simple answer', required=())), ('multiple_answer', wagtail.blocks.StructBlock([('reduction', wagtail.blocks.BooleanBlock(help_text='Check this box if you want to create a smaller version of choice answer (Perfect for the choices inside another choice answer)', label='Size reduction', required=False)), ('choices', wagtail.blocks.ListBlock(utils.faq.ChoiceBlock, help_text='Cliquez sur le + ci-dessous pour ajouter une option dans vos conditions', label='Ajouter une option'))])), ('step_answer', wagtail.blocks.StructBlock([('ordonnated', wagtail.blocks.BooleanBlock(help_text='Check this box if you want to create an ordonnated version of step answer (Step 1, Step 2, Step 3, etc.)', label='Ordonnated steps', required=False)), ('steps', wagtail.blocks.ListBlock(utils.faq.StepBlock, help_text='Cliquez sur le + ci-dessous pour ajouter un élément dans votre liste', label='Ajouter un élément'))]))], blank=True, help_text='Click on the ⊕ below to add an answer. You can add simple answer(s), conditional answer(s) or step answer(s). You can either imbriqued conditional answer(s) or step answer(s) inside any answer.', null=True, verbose_name='Answer(s)'),
        ),
    ]
