# Generated by Django 5.0 on 2024-03-05 07:21

import home.models
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compterendupage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('media', home.models.MediaBlock(icon='media')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full')), ('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(help_text='Enter the URL.', label='URL')), ('text', wagtail.blocks.CharBlock(help_text='Enter the visible text for this link (optional).', label='Replacement Text', required=False))], icon='link')), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.embeds.blocks.EmbedBlock(label='URL a intégrer')), ('resolution', wagtail.blocks.ChoiceBlock(choices=[('very_small', 'Very small'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('very_large', 'Very large')], label='Size of the frame')), ('alternative_title', wagtail.blocks.CharBlock(blank=True, help_text='Alternative title for users accessibility.', label='Alternative title', required=False))], icon='media')), ('list', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(icon='list-ul'), icon='list-ul')), ('quote', wagtail.blocks.BlockQuoteBlock(icon='openquote')), ('table', wagtail.contrib.table_block.blocks.TableBlock(icon='table')), ('chart', wagtail.blocks.StreamBlock([('chart_block', wagtail.blocks.StructBlock([('chart_type', wagtail.blocks.ChoiceBlock(choices=[('line', 'Line Chart'), ('bar', 'Vertical Bar Chart'), ('bar_horizontal', 'Horizontal Bar Chart'), ('area', 'Area Chart'), ('multi', 'Combo Line/Bar/Area Chart'), ('pie', 'Pie Chart'), ('doughnut', 'Doughnut Chart'), ('radar', 'Radar Chart'), ('polar', 'Polar Chart'), ('waterfall', 'Waterfall Chart')], label='Chart Type')), ('title', wagtail.blocks.CharBlock(required=False)), ('datasets', wagtail.blocks.TextBlock(default='{"data":[], "options":{}}')), ('settings', wagtail.blocks.StructBlock([('show_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Show legend', required=False)), ('html_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Use HTML legend', required=False)), ('legend_position', wagtail.blocks.ChoiceBlock(choices=[('top', 'Top'), ('bottom', 'Bottom'), ('left', 'Left'), ('right', 'Right')], group='General', label='Legend position')), ('reverse_legend', wagtail.blocks.BooleanBlock(default=False, group='General', label='Reverse legend', required=False)), ('show_values_on_chart', wagtail.blocks.BooleanBlock(default=False, group='General', label='Show values on chart', required=False)), ('precision', wagtail.blocks.IntegerBlock(default=1, group='General', label='Precision in labels/tooltips')), ('show_grid', wagtail.blocks.BooleanBlock(default=True, group='General', label='Show Chart Grid', required=False)), ('x_label', wagtail.blocks.CharBlock(group='General', label='X axis label', required=False)), ('stacking', wagtail.blocks.ChoiceBlock(choices=[('none', 'No stacking'), ('stacked', 'Stacked'), ('stacked_100', 'Stacked 100%')], group='General', label='Stacking')), ('unit_override', wagtail.blocks.CharBlock(group='General', label='Unit override', required=False)), ('y_left_min', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis minimum value', required=False)), ('y_left_max', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis maximum value', required=False)), ('y_left_step_size', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis step size', required=False)), ('y_left_label', wagtail.blocks.CharBlock(group='Left_Axis', label='Left Y axis label', required=False)), ('y_left_data_type', wagtail.blocks.ChoiceBlock(choices=[('number', 'Numerical'), ('percentage', 'Percentage')], group='Left_Axis', label='Left Y axis data type', required=False)), ('y_left_precision', wagtail.blocks.IntegerBlock(default=0, group='Left_Axis', label='Left Y axis tick precision')), ('y_left_show', wagtail.blocks.BooleanBlock(default=True, group='Left_Axis', label='Show left axis numbers', required=False)), ('y_right_min', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis minimum value', required=False)), ('y_right_max', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis maximum value', required=False)), ('y_right_step_size', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis step size', required=False)), ('y_right_label', wagtail.blocks.CharBlock(group='Right_Axis', label='Right Y axis label', required=False)), ('y_right_data_type', wagtail.blocks.ChoiceBlock(choices=[('number', 'Numerical'), ('percentage', 'Percentage')], group='Right_Axis', label='Right Y axis data type', required=False)), ('y_right_precision', wagtail.blocks.IntegerBlock(default=0, group='Right_Axis', label='Right Y axis tick precision')), ('y_right_show', wagtail.blocks.BooleanBlock(default=True, group='Right_Axis', label='Show right axis numbers', required=False)), ('pie_border_width', wagtail.blocks.IntegerBlock(default=2, group='Pie_Chart', label='Width of pie slice border')), ('pie_border_color', wagtail.blocks.CharBlock(default='#fff', group='Pie_Chart', label='Color of pie slice border'))]))], chart_type=(('line', 'Graphique linéaire'), ('bar', 'Graphique à barres verticales'), ('bar_horizontal', 'Graphique à barres horizontales'), ('area', 'Graphique en aires'), ('multi', 'Graphique combiné linéaire/barres/aires'), ('pie', 'Graphique en secteurs'), ('doughnut', 'Graphique en anneau'), ('radar', 'Graphique radar'), ('polar', 'Graphique polaire'), ('waterfall', 'Graphique en cascade')), colors=(('#ff0000', 'Rouge'), ('#00ff00', 'Vert'), ('#0000ff', 'Bleu'), ('#ffff00', 'Jaune'), ('#ff00ff', 'Magenta'), ('#00ffff', 'Cyan'), ('#808080', 'Gris'), ('#800000', 'Marron'), ('#008000', 'Vert foncé'), ('#000080', 'Bleu foncé'), ('#800080', 'Violet'), ('#c0c0c0', 'Argent'), ('#ff3399', 'Rose'), ('#008080', 'Sarcelle'), ('#00CED1', 'Turquoise foncé'), ('#7CFC00', 'Vert prairie'), ('#D2691E', 'Chocolat'), ('#48D1CC', 'Turquoise moyen'), ('#BDB76B', 'Kaki foncé'), ('#3CB371', 'Vert mer moyen'), ('#66CDAA', 'Aquamarine moyen'), ('#FF7F50', 'Corail'))))], icon='chart')), ('PDF', wagtail.blocks.StructBlock([('pdf_document', wagtail.documents.blocks.DocumentChooserBlock(help_text='Chose a PDF wich will be converted to images and added in the flow. Name smartly the document, it will be used to create a collection.', label='Document', required=True)), ('pdf_import', wagtail.blocks.BooleanBlock(default=False, help_text='Use cautiously. It will override all existing images in this section.', label='Save and import', required=False)), ('pdf_images', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(required=False), form_classname='collapsible, collapsed', help_text='You can remove or replace any of the images below. If you want to restore the original images, click again on the import button.', label='Aperçu des pages', required=False))], icon='doc-full')), ('DOCX', wagtail.blocks.StructBlock([('docx_document', wagtail.documents.blocks.DocumentChooserBlock(help_text='Chose a DOCX file to import in the flow.', label='Document', required=True)), ('docx_import', wagtail.blocks.BooleanBlock(default=False, help_text='Use cautiously. It will override all existing content in this section.', label='Save and import', required=False)), ('docx_content', wagtail.blocks.StreamBlock([('heading', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(label='content', required=True)), ('heading_level', wagtail.blocks.ChoiceBlock(choices=[('h1', 'Heading 1'), ('h2', 'Heading 2'), ('h3', 'Heading 3'), ('h4', 'Heading 4'), ('h5', 'Heading 5'), ('h6', 'Heading 6')], label='level', required=False)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False))])), ('paragraph', wagtail.blocks.StructBlock([('paragraph', wagtail.blocks.RichTextBlock(label='content', required=True)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False))])), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='content', required=True)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('icon', 'Icon'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('full', 'Full')], label='size', required=False))])), ('table', wagtail.blocks.StructBlock([('table', wagtail.contrib.table_block.blocks.TableBlock(label='content', required=True)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right'), ('justify', 'Justify')], required=False))]))], classname='collapsible, collapsed', help_text='You can remove or replace any of the content below. If you want to restore the original content, click again on the import button.', label='Aperçu du contenu', required=False))], icon='doc-full'))], blank=True, help_text='This is the main content of the page.', null=True, verbose_name='Agenda'),
        ),
    ]
