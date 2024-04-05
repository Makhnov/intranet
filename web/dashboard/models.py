from django import forms
from django.db import models
from wagtail.admin.ui.components import Component
from django.db import models
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.images import get_image_model_string

# Traduction
from django.utils.translation import gettext_lazy as _

@register_setting(icon='doc-full-inverse')
class PDFSettings(BaseSiteSetting):    
    max_items = 1
    
    # Widgets pour les champs d'ouverture
    opening_councils_widget = forms.Textarea(attrs={
        'placeholder': "Cher(e) Collègue,\n\n"
                    "J’ai l’honneur de vous inviter au premier conseil communautaire de l’année 2023 qui aura lieu le :",
        'rows': 3,
    })

    opening_boards_widget = forms.Textarea(attrs={
        'placeholder': "Cher(e) Collègue,\n\n"
                    "J’ai l’honneur de vous inviter au premier bureau de l’année 2023 qui aura lieu le :",
        'rows': 3,
    })

    opening_commissions_widget = forms.Textarea(attrs={
        'placeholder': "Cher(e) Collègue,\n\n"
                    "J’ai l’honneur de vous inviter à la première commission de l’année 2023 qui aura lieu le :",
        'rows': 3,
    })

    opening_conferences_widget = forms.Textarea(attrs={
        'placeholder': "Cher(e) Collègue,\n\n"
                    "J’ai l’honneur de vous inviter à la première conférence des maires de l’année 2023 qui aura lieu le :",
        'rows': 3,
    })

    # Widgets pour les champs de fermeture
    closing_councils_widget = forms.Textarea(attrs={
        'placeholder': "Je vous prie d’agréer, Cher(e) Collègue, l’expression de mes sentiments dévoués.",
        'rows': 3,
    })

    closing_boards_widget = forms.Textarea(attrs={
        'placeholder': "Je vous prie d’agréer, Cher(e) Collègue, l’expression de mes sentiments dévoués.",
        'rows': 3,
    })

    closing_commissions_widget = forms.Textarea(attrs={
        'placeholder': "Je vous prie d’agréer, Cher(e) Collègue, l’expression de mes sentiments dévoués.",
        'rows': 3,
    })

    closing_conferences_widget = forms.Textarea(attrs={
        'placeholder': "Je vous prie d’agréer, Monsieur (Madame) le (la) maire, l’expression de mes sentiments dévoués.",
        'rows': 3,
    })

    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Logo")
    )
    footer_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Footer Image")
    )
    watermark = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Watermark")
    )
    locality = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Locality for the letter.'),
        verbose_name=_("Locality")
    )
    locality_description = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Locality description for the letter.'),
        verbose_name=_("Locality Description")
    )
    
    panels = [
        FieldPanel('logo', heading=_("Header logo")),
        FieldPanel('footer_image', heading=_("Footer image")),
        FieldPanel('watermark', heading=_("Watermark")),
        FieldPanel('locality', heading=_("Locality")),
        FieldPanel('locality_description', heading=_("Locality Description")),
        MultiFieldPanel(
            [
                FieldPanel('opening_councils', classname="col6", widget=opening_councils_widget, heading=_("Opening Councils")),
                FieldPanel('opening_boards', classname="col6", widget=opening_boards_widget, heading=_("Opening Boards")),
                FieldPanel('opening_commissions', classname="col6", widget=opening_commissions_widget, heading=_("Opening Commissions")),
                FieldPanel('opening_conferences', classname="col6", widget=opening_conferences_widget, heading=_("Opening Conferences")),
            ],
            heading=_("Openings"),
            classname="collapsible, collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('closing_councils', classname="col6", widget=closing_councils_widget, heading=_("Closing Councils")),
                FieldPanel('closing_boards', classname="col6", widget=closing_boards_widget, heading=_("Closing Boards")),
                FieldPanel('closing_commissions', classname="col6", widget=closing_commissions_widget, heading=_("Closing Commissions")),
                FieldPanel('closing_conferences', classname="col6", widget=closing_conferences_widget, heading=_("Closing Conferences")),
            ],
            heading=_("Closings"),
            classname="collapsible, collapsed"
        ),
    ]

    # Opening fields
    opening_councils = models.TextField(
        blank=True,
        help_text=_('Text for council openings.'),
        default="Cher(e) Collègue,\n\n"
                "J’ai l’honneur de vous inviter au premier conseil communautaire de l’année 2023 qui aura lieu le :",
        verbose_name=_("Opening Councils")
    )
    opening_boards = models.TextField(
        blank=True,
        help_text=_('Text for board openings.'),
        default="Cher(e) Collègue,\n\n"
                "J’ai l’honneur de vous inviter au premier bureau de l’année 2023 qui aura lieu le :",
        verbose_name=_("Opening Boards")
    )
    opening_commissions = models.TextField(
        blank=True,
        help_text=_('Text for commission openings.'),
        default="Cher(e) Collègue,\n\n"
                "J’ai l’honneur de vous inviter à la première commission de l’année 2023 qui aura lieu le :",
        verbose_name=_("Opening Commissions")
    )
    opening_conferences = models.TextField(
        blank=True,
        help_text=_('Text for conference openings.'),
        default="Cher(e) Collègue,\n\n"
                "J’ai l’honneur de vous inviter à la première conférence des maires de l’année 2023 qui aura lieu le :",
        verbose_name=_("Opening Conferences")
    )

    # Closing fields
    closing_councils = models.TextField(
        blank=True,
        help_text=_('Closing text for councils.'),
        default="Je vous prie d’agréer, Cher(e) Collègue, l’expression de mes sentiments dévoués.",
        verbose_name=_("Closing Councils")
    )
    closing_boards = models.TextField(
        blank=True,
        help_text=_('Closing text for boards.'),
        default="Je vous prie d’agréer, Cher(e) Collègue, l’expression de mes sentiments dévoués.",
        verbose_name=_("Closing Boards")
    )
    closing_commissions = models.TextField(
        blank=True,
        help_text=_('Closing text for commissions.'),
        default="Je vous prie d’agréer, Cher(e) Collègue, l’expression de mes sentiments dévoués.",
        verbose_name=_("Closing Commissions")
    )
    closing_conferences = models.TextField(
        blank=True,
        help_text=_('Closing text for conferences.'),
        default="Je vous prie d’agréer, Monsieur (Madame) le (la) maire, l’expression de mes sentiments dévoués.",
        verbose_name=_("Closing Conferences")
    )

    class Meta:
        verbose_name = 'PDF Settings'

@register_setting(icon='image')
class IntranetIcons(BaseSiteSetting):    
    max_items = 1

    # PAGES
    convocation = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Convocation page")
    )
    compte_rendu = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Compte rendu page")
    )
    all_faq = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("All FAQ"),
        verbose_name=_("All FAQ")
    )    
    law_text = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',        
        verbose_name=_("Law text"),
        help_text=_("FAQ page, law text icon"),    
    )
    tags = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Tags"),
        help_text=_("Tag icon for numerous pages"),
    )
    amicale_news = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Amicale news"),
    )
    amicale_sorties = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Amicale sorties"),
    )
    amicale_divers = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Amicale divers")
    )
    amicale_none = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Amicale unknown"),
        help_text=_("Amicale unknown page type icon"),
    )      
    generic = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Web page"),
        verbose_name=_("Web page")
    )
    instant_download = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Documents (InstantDownload)"),
        verbose_name=_("Download")
    )
    form = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Form"),
        verbose_name=_("Form")
    )       
    site_web = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Site web officiel")
    )
    office_tourisme = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Office de tourisme")
    )
    facebook_icon = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Facebook")
    )

    # NAVIGATION
    home = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Home"),
        help_text=_("'Home' symbol to back to the index section. Related Index Pages : 'Calendar', 'Amicale', 'FAQ', 'Administration'. ")
    )
    user_profile = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("User profile"),
        verbose_name=_("Header top-right icon")
    )
    previous_item = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Previous Item"),
        help_text=_("Footer icon to nvaigate (left) in the list"),
    )    
    next_item = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Next Item"),
        help_text=_("Footer icon to nvaigate (right) in the list"),
    )

    # DISPLAY
    open = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Open")
    )
    close = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Close") 
    ) 
    more = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("More") 
    )    
    less = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Less") 
    )
    more_right = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("More (right)")
    )        
    less_left = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Less (left)")
    )

    # ACTION$
    search = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Search"),
        verbose_name=_("Search")
    )
    zoom_in = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Zoom in"),
        verbose_name=_("Zoom in")
    )
    zoom_out = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Zoom out"),
        verbose_name=_("Zoom out")
    )
    apply_filter = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Apply filter"),
        verbose_name=_("Apply filter")
    )
    reset_filter = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Reset filter"),
        verbose_name=_("Reset filter")
    )
    copy = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Copy to clipboard"),
        verbose_name=_("Copy to clipboard")
    )
    download = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Download"),
        verbose_name=_("Download")
    )
    print = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Print"),
        verbose_name=_("Print")
    )

    # LISTE
    ul_item = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Unordered list item"),
        help_text=_("Icon preceding the item label"),
    )
    ol_item_1 = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("OL-1"),
        help_text=_("Ordered list first item"),
    )
    ol_item_2 = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("OL-2"),
        help_text=_("Ordered list item"),
    )
    ol_item_3 = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("OL-3"),
        help_text=_("Ordered list item"),
    )
    ol_item_4 = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("OL-4"),
        help_text=_("Ordered list item"),
    )
    ol_item_5 = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("OL-5"),
        help_text=_("Ordered list item"),
    )
    ol_item_6 = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("OL-6"),
        help_text=_("Ordered list item"),
    )
    ol_item_7 = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("OL-7"),
        help_text=_("Ordered list item"),
    )
    ol_item_8 = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("OL-8"),
        help_text=_("Ordered list item"),
    )
    ol_item_9 = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("OL-9"),
        help_text=_("Ordered list item"),
    )  

    # CALENDRIER
    list_view = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("List view"),
        verbose_name=_("List view")
    )
    day_view = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Day view"),
        verbose_name=_("Day view")
    )
    week_view = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Week view"),
        verbose_name=_("Week view")
    )
    month_view = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Month view"),
        verbose_name=_("Month view")
    )
    this_view = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Actual view"),
        verbose_name=_("Actual view")
    )
    calendar_previous_page = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Previous Page"),
        help_text=_("Icon in the calendar section to go to the previous page")
    )
    calendar_next_page = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Next Page"),
        help_text=_("Icon in the calendar section to go to the next page"),
    )
    upcoming_view = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Upcoming view"),
        verbose_name=_("Upcoming view")
    )
    past_view = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Past view"),
        verbose_name=_("Past view")
    )       

    # CONTENT PANEL
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('convocation', heading=_("Convocation page")),
                FieldPanel('compte_rendu', heading=_("Compte rendu page")),
                FieldPanel('all_faq', heading=_("All FAQ")),
                FieldPanel('law_text', heading=_("Law text")),
                FieldPanel('tags', heading=_("Tags")),
                FieldPanel('amicale_news', heading=_("Amicale news")),
                FieldPanel('amicale_sorties', heading=_("Amicale sorties")),
                FieldPanel('amicale_divers', heading=_("Amicale divers")),
                FieldPanel('amicale_none', heading=_("Amicale unknown")),
                FieldPanel('generic', heading=_("Web page")),
                FieldPanel('instant_download', heading=_("Documents (InstantDownload)")),
                FieldPanel('form', heading=_("Form")),
                FieldPanel('site_web', heading=_("Site web officiel")),
                FieldPanel('office_tourisme', heading=_("Office de tourisme")),
                FieldPanel('facebook_icon', heading=_("Facebook")),
            ],
            heading=_("Pages"),
            classname="collapsible, collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('home', heading=_("Home")),
                FieldPanel('user_profile', heading=_("User Profile")),
                FieldPanel('previous_item', heading=_("Previous Item")),
                FieldPanel('next_item', heading=_("Next Item")),
            ],
            heading=_("Navigation"),
            classname="collapsible, collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('open', heading=_("Open")),
                FieldPanel('close', heading=_("Close")),
                FieldPanel('more', heading=_("More")),
                FieldPanel('less', heading=_("Less")),
                FieldPanel('more_right', heading=_("More (right)")),
                FieldPanel('less_left', heading=_("Less (left)")),
            ],
            heading=_("Display"),
            classname="collapsible, collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('search', heading=_("Search")),
                FieldPanel('zoom_in', heading=_("Zoom in")),
                FieldPanel('zoom_out', heading=_("Zoom out")),
                FieldPanel('apply_filter', heading=_("Apply filter")),
                FieldPanel('reset_filter', heading=_("Reset filter")),
                FieldPanel('copy', heading=_("Copy to clipboard")),
                FieldPanel('download', heading=_("Download")),
                FieldPanel('print', heading=_("Print")),
            ],
            heading=_("Actions"),
            classname="collapsible, collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('ul_item', heading=_("Unordered list item")),
                FieldPanel('ol_item_1', heading=_("Ordered list item 1")),
                FieldPanel('ol_item_2', heading=_("Ordered list item 2")),
                FieldPanel('ol_item_3', heading=_("Ordered list item 3")),
                FieldPanel('ol_item_4', heading=_("Ordered list item 4")),
                FieldPanel('ol_item_5', heading=_("Ordered list item 5")),
                FieldPanel('ol_item_6', heading=_("Ordered list item 6")),
                FieldPanel('ol_item_7', heading=_("Ordered list item 7")),
                FieldPanel('ol_item_8', heading=_("Ordered list item 8")),
                FieldPanel('ol_item_9', heading=_("Ordered list item 9")),
            ],
            heading=_("List"),
            classname="collapsible, collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('list_view', heading=_("List view")),
                FieldPanel('day_view', heading=_("Day view")),
                FieldPanel('week_view', heading=_("Week view")),
                FieldPanel('month_view', heading=_("Month view")),
                FieldPanel('this_view', heading=_("Actual view")),
                FieldPanel('calendar_previous_page', heading=_("Previous Page")),
                FieldPanel('calendar_next_page', heading=_("Next Page")),
                FieldPanel('upcoming_view', heading=_("Upcoming view")),
                FieldPanel('past_view', heading=_("Past view")),
            ],
            heading=_("Calendar"),
            classname="collapsible, collapsed"
        ),
    ]
    
    class Meta:
        verbose_name = 'Intranet icons'
