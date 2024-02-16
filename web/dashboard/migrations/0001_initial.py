# Generated by Django 5.0 on 2024-02-14 11:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0092_query_searchpromotion_querydailyhits'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntranetIcons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('administration', models.ForeignKey(blank=True, help_text='Administration page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Administration')),
                ('all_faq', models.ForeignKey(blank=True, help_text='All FAQ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='All FAQ')),
                ('amicale', models.ForeignKey(blank=True, help_text='Amicale page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Amicale')),
                ('amicale_divers', models.ForeignKey(blank=True, help_text='Amicale divers', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Amicale divers')),
                ('amicale_news', models.ForeignKey(blank=True, help_text='Amicale news', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Amicale news')),
                ('amicale_none', models.ForeignKey(blank=True, help_text='Amicale unknown', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Amicale unknown')),
                ('amicale_sorties', models.ForeignKey(blank=True, help_text='Amicale sorties', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Amicale sorties')),
                ('apply_filter', models.ForeignKey(blank=True, help_text='Apply filter', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Apply filter')),
                ('base_item', models.ForeignKey(blank=True, help_text='Base item', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Base Item')),
                ('close', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Close')),
                ('compte_rendu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Compte rendu page')),
                ('convocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Convocation page')),
                ('day_view', models.ForeignKey(blank=True, help_text='Day view', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Day view')),
                ('download', models.ForeignKey(blank=True, help_text='Documents (InstantDownload)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Download')),
                ('facebook_icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Facebook')),
                ('faq', models.ForeignKey(blank=True, help_text='FAQ page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='FAQ')),
                ('form', models.ForeignKey(blank=True, help_text='Form', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Form')),
                ('generic', models.ForeignKey(blank=True, help_text='Web page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Web page')),
                ('home', models.ForeignKey(blank=True, help_text="'Home' symbol to back to the index section. Related Index Pages : 'Calendar', 'Amicale', 'FAQ', 'Administration'. ", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Home')),
                ('less', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Less')),
                ('less_left', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Less (left)')),
                ('list_view', models.ForeignKey(blank=True, help_text='List view', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='List view')),
                ('month_view', models.ForeignKey(blank=True, help_text='Month view', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Month view')),
                ('more', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='More')),
                ('more_right', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='More (right)')),
                ('next_item', models.ForeignKey(blank=True, help_text='Next item', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Next Item')),
                ('next_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Next Page')),
                ('office_tourisme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Office de tourisme')),
                ('open', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Open')),
                ('past_view', models.ForeignKey(blank=True, help_text='Past view', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Past view')),
                ('previous_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Previous Item')),
                ('previous_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Previous Page')),
                ('reset_filter', models.ForeignKey(blank=True, help_text='Reset filter', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Reset filter')),
                ('ressources', models.ForeignKey(blank=True, help_text='Ressources page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Ressources')),
                ('search', models.ForeignKey(blank=True, help_text='Search', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Search')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
                ('site_web', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Site web officiel')),
                ('this_view', models.ForeignKey(blank=True, help_text='Actual view', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Actual view')),
                ('upcoming_view', models.ForeignKey(blank=True, help_text='Upcoming view', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Upcoming view')),
                ('user_profile', models.ForeignKey(blank=True, help_text='User profile', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='User Profile')),
                ('week_view', models.ForeignKey(blank=True, help_text='Week view', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Week view')),
                ('zoom_in', models.ForeignKey(blank=True, help_text='Zoom in', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Zoom in')),
                ('zoom_out', models.ForeignKey(blank=True, help_text='Zoom out', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Zoom out')),
            ],
            options={
                'verbose_name': 'Intranet icons',
            },
        ),
        migrations.CreateModel(
            name='PDFSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locality', models.CharField(blank=True, help_text='Locality for the letter.', max_length=255, verbose_name='Locality')),
                ('locality_description', models.CharField(blank=True, help_text='Locality description for the letter.', max_length=255, verbose_name='Locality Description')),
                ('opening_councils', models.TextField(blank=True, default='Cher(e) Collègue,\n\nJ’ai l’honneur de vous inviter au premier conseil communautaire de l’année 2023 qui aura lieu le :', help_text='Text for council openings.', verbose_name='Opening Councils')),
                ('opening_boards', models.TextField(blank=True, default='Cher(e) Collègue,\n\nJ’ai l’honneur de vous inviter au premier bureau de l’année 2023 qui aura lieu le :', help_text='Text for board openings.', verbose_name='Opening Boards')),
                ('opening_commissions', models.TextField(blank=True, default='Cher(e) Collègue,\n\nJ’ai l’honneur de vous inviter à la première commission de l’année 2023 qui aura lieu le :', help_text='Text for commission openings.', verbose_name='Opening Commissions')),
                ('opening_conferences', models.TextField(blank=True, default='Cher(e) Collègue,\n\nJ’ai l’honneur de vous inviter à la première conférence des maires de l’année 2023 qui aura lieu le :', help_text='Text for conference openings.', verbose_name='Opening Conferences')),
                ('closing_councils', models.TextField(blank=True, default='Je vous prie d’agréer, Cher(e) Collègue, l’expression de mes sentiments dévoués.', help_text='Closing text for councils.', verbose_name='Closing Councils')),
                ('closing_boards', models.TextField(blank=True, default='Je vous prie d’agréer, Cher(e) Collègue, l’expression de mes sentiments dévoués.', help_text='Closing text for boards.', verbose_name='Closing Boards')),
                ('closing_commissions', models.TextField(blank=True, default='Je vous prie d’agréer, Cher(e) Collègue, l’expression de mes sentiments dévoués.', help_text='Closing text for commissions.', verbose_name='Closing Commissions')),
                ('closing_conferences', models.TextField(blank=True, default='Je vous prie d’agréer, Monsieur (Madame) le (la) maire, l’expression de mes sentiments dévoués.', help_text='Closing text for conferences.', verbose_name='Closing Conferences')),
                ('footer_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Footer Image')),
                ('logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Logo')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
                ('watermark', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage', verbose_name='Watermark')),
            ],
            options={
                'verbose_name': 'PDF Settings',
            },
        ),
    ]