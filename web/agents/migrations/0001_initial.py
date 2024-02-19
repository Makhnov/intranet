# Generated by Django 5.0 on 2024-02-14 11:16

import agents.models
import django.db.models.deletion
import home.models
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Visible title on the FAQ index page.', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(default='', editable=False, unique=True)),
                ('tooltip', models.CharField(blank=True, help_text='Tooltip displayed on the index pages. Visible when user mouse over the logo icon.', max_length=255, null=True, verbose_name='Tooltip')),
                ('logo', models.ForeignKey(blank=True, help_text='Visible icon on index pages. Ideal size: 1/1 (square or round). Format :⚠️SVG⚠️', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Logo')),
            ],
            options={
                'verbose_name': 'one category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='FaqIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('heading', models.CharField(blank=True, help_text='Displayed in menus, the heading is the title of the page.', max_length=255, null=True, verbose_name='Heading')),
                ('tooltip', models.CharField(blank=True, help_text='Used for accessibility (alt, title) and when user mouse over the icon.', max_length=255, null=True, verbose_name='Tooltip')),
                ('logo', models.ForeignKey(blank=True, help_text='𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦: Round or square (1/1). 𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦𝐚𝐭: Filled SVG. 𝐒𝐞𝐜𝐨𝐧𝐝𝐚𝐫𝐲 𝐟𝐨𝐫𝐦𝐚𝐭: PNG with transparent background.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Logo (SVG, png, jpg, etc.)')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FaqPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('question', models.CharField(max_length=255, verbose_name='Question')),
                ('answer', wagtail.fields.StreamField([('single_answer', wagtail.blocks.StreamBlock([('heading', wagtail.blocks.CharBlock(form_classname='title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('media', home.models.MediaBlock(icon='media')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full')), ('link', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(help_text='Enter the URL.', label='URL')), ('text', wagtail.blocks.CharBlock(help_text='Enter the visible text for this link (optional).', label='Replacement Text', required=False))], icon='link')), ('embed', wagtail.blocks.StructBlock([('embed_url', wagtail.embeds.blocks.EmbedBlock(label='URL a intégrer')), ('resolution', wagtail.blocks.ChoiceBlock(choices=[('very_small', 'Very small'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('very_large', 'Very large')], label='Size of the frame')), ('alternative_title', wagtail.blocks.CharBlock(blank=True, help_text='Alternative title for users accessibility.', label='Alternative title', required=False))], icon='media')), ('list', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(icon='list-ul'), icon='list-ul')), ('quote', wagtail.blocks.BlockQuoteBlock(icon='openquote')), ('table', wagtail.contrib.table_block.blocks.TableBlock(icon='table'))], icon='doc-full', label='Simple answer', required=False)), ('multiple_answer', wagtail.blocks.StructBlock([('choices_intro', wagtail.blocks.CharBlock(icon='pilcrow', label='Introduction', required=False, search_index=True)), ('choices', wagtail.blocks.ListBlock(agents.models.ChoiceBlock, label='Click on the + below to add another condition'))], icon='help', label='Conditonnal answer')), ('step_answer', wagtail.blocks.StructBlock([('steps_intro', wagtail.blocks.CharBlock(icon='pilcrow', label='Introduction', required=False, search_index=True)), ('steps', wagtail.blocks.ListBlock(agents.models.StepBlock, label='Click on the + below to add another step'))], icon='tasks', label='Step answer'))], blank=True, help_text='Click on the ⊕ below to add an answer. You can add simple answer(s), conditional answer(s) or step answer(s). You can either imbriqued conditional answer(s) or step answer(s) inside any answer.', null=True, verbose_name='Answer(s)')),
                ('related', wagtail.fields.StreamField([('related_faq', wagtail.blocks.PageChooserBlock(label='Related FAQ', page_type=['agents.FaqPage']))], blank=True, help_text="You can click on the ⊕ below to add related FAQ to this one. Users will see it in the 'Go further' section", null=True, verbose_name='Similar themes')),
                ('law_texts', wagtail.fields.StreamField([('law_text', wagtail.blocks.StructBlock([('text_name', wagtail.blocks.CharBlock(label='Law text reference', max_length=255, required=True)), ('text_link', wagtail.blocks.URLBlock(label='Law text link', required=True))]))], blank=True, help_text='You can click on the ⊕ below to add law texts related to this FAQ.', null=True, verbose_name='Law texts')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='agents.faqcategory', verbose_name='Category')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FaqPageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='agents.faqpage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='faqpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='agents.FaqPageTag', to='taggit.Tag', verbose_name='Faq Tags'),
        ),
    ]
