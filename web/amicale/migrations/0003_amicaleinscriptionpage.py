# Generated by Django 5.0 on 2024-04-14 10:37

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtailstreamforms.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amicale', '0002_alter_amicalepage_type'),
        ('images', '0001_initial'),
        ('wagtailcore', '0092_query_searchpromotion_querydailyhits'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmicaleInscriptionPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('heading', models.CharField(blank=True, help_text='Displayed in menus, the heading is the title of the page.', max_length=255, null=True, verbose_name='Heading')),
                ('tooltip', models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip')),
                ('inscription_form', wagtail.fields.StreamField([('form_field', wagtail.blocks.StructBlock([('form', wagtailstreamforms.blocks.FormChooserBlock()), ('form_action', wagtail.blocks.CharBlock(help_text='The form post action. "" or "." for the current page or a url', required=False)), ('form_reference', wagtailstreamforms.blocks.InfoBlock(help_text='This form will be given a unique reference once saved', required=False))], icon='form', label='Form field'))], blank=True, help_text='Add an inscription form for this event.', null=True, verbose_name='Inscription form')),
                ('logo', models.ForeignKey(blank=True, help_text='𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦: Round or square (1/1). 𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦𝐚𝐭: Filled SVG. 𝐒𝐞𝐜𝐨𝐧𝐝𝐚𝐫𝐲 𝐟𝐨𝐫𝐦𝐚𝐭: PNG with transparent background.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Logo (SVG, png, jpg, etc.)')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
