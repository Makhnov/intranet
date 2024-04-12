from termcolor import colored
from django.db import models
from django.utils.timezone import datetime
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

# Page de menu
from utils.menu_pages import MenuPage, menu_page_save

# Snippets
from wagtail.snippets.models import register_snippet

# Blocks, Medias, PJ, etc.
from utils.widgets import GalleryImage, PiecesJointes as PJBlock
from utils.streamfield import (
    CustomMediaBlock as MediaBlock,
    CustomLinkBlock as LinkBlock,
    CustomEmbedBlock as EmbedBlock,
    CustomPDFBlock as PDFBlock,
    CustomDOCXBlock as DOCXBlock,
)

# Wagtail Geo Widget
from django.utils.functional import cached_property
from wagtailgeowidget import geocoders
from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from wagtailgeowidget.panels import GeoAddressPanel, LeafletPanel

# API
from wagtail.api import APIField

# Traduction
from django.utils.translation import gettext_lazy as _

# Recherche
from wagtail.search import index

# Formulaire
from wagtailstreamforms.blocks import WagtailFormBlock

##################
## PAGE DE MENU ##
################## 

# Index pour toutes les pages de l'amicale (quel que soit le type)
class AmicaleIndexPage(MenuPage):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["amicale.AmicalePage"]
    save = menu_page_save("amicale")
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        amicalepages = AmicalePage.objects.child_of(self).live()

        query = request.GET.get('query', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        article_type = request.GET.get('type', None)
        
        # print(colored(article_type, 'green'))
        # print(colored(start_date, 'green'))
        # print(colored(end_date, 'green'))
        # print(colored(query, 'green'))
                      
        if query:
            amicalepages = amicalepages.filter(title__icontains=query)

        if start_date:
            amicalepages = amicalepages.filter(date__gte=start_date)

        if end_date:
            amicalepages = amicalepages.filter(date__lte=end_date)

        if article_type and article_type != '*':
            amicalepages = amicalepages.filter(type=article_type)

        # Tri par type pour regroupement dans le template
        amicalepages = amicalepages.order_by('type', '-date')

        is_root = not (start_date or end_date or article_type or query)
        
        # Préparation des blocs par type
        context['search_query'] = query
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['article_type'] = article_type
        context['amicale_news'] = amicalepages.filter(type='news')
        context['amicale_sorties'] = amicalepages.filter(type='sorties')
        context['amicale_divers'] = amicalepages.filter(type='autres')
        context['is_root'] = is_root
        context['fields'] = ['type', 'date']
        context['section'] = 'amicale'
        
        return context

#######################
## PAGE DE L'AMICALE ##
####################### 

# Page générique pour les articles (quel que soit le type)
class AmicalePage(Page):
    parent_page_types = ["amicale.AmicaleIndexPage"]

    type = models.CharField(
        max_length=10,
        choices=[
            ('autres', 'Divers'),
            ('sorties', 'Sorties'),
            ('news', 'Nouvelles'),
        ],
        null=True,
        blank=True,
        default='autres',
        verbose_name="Type de l'article",
    )
    date = models.DateField(
        verbose_name=_("Date"),
        help_text=_("For an event enter the event date, for an article enter the publication date(or leave it blank)."),
        null=True,
        blank=True,
        default=datetime.now,
    )
    author = models.ForeignKey(
        'Author',
        verbose_name=_("Auteur"),
        null=True,
        blank=True,
        default=1,
        on_delete=models.SET_NULL,
    )
    tags = ClusterTaggableManager(
        through='AmicalePageTag',
        blank=True,
        verbose_name=_("Amicale Tags"),
    )
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title", icon="title", label=_("Heading"))),
            ("paragraph", blocks.RichTextBlock(icon="pilcrow", label=_("Paragraph"))),
            ("media", MediaBlock(icon="media", label=_("Media"))),            
            ("image", ImageChooserBlock(icon="image", label=_("Image"))),
            ('document', DocumentChooserBlock(icon="doc-full-inverse", label=_("Document"))),            
            ("link", LinkBlock(icon="link", label=_("Link"))),
            ("embed", EmbedBlock(icon="media", label=_("Embed media"))),
            ("list", blocks.ListBlock(blocks.CharBlock(icon="radio-full", label=_("Item")), icon="list-ul", label=_("List"))),
            ("quote", blocks.BlockQuoteBlock(icon="openquote", label=_("Quote"))),
        ],
        use_json_field=True,
        blank=True,
        null=True,
        verbose_name=_("Agenda"),
        help_text=_("This is the main content of the page."),
    )
    use_map = models.BooleanField(
        default=False,
        verbose_name=_("Use a map?"),
        help_text=_("Check this box if you want to use a map."),
    )
    location = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name=_("Location"),
        help_text=_("Select location on the map."),
    )
    address = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name=_("Address"),
        help_text=_("Address to geocode to get the location."),
    )
    point_name = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text=_("Name to display for this point on the map."),
    )
    point_link = models.URLField(
        blank=True,
        null=True,
        help_text=_("Link for the point on the map."),
    )

    @cached_property
    def point(self):
        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point["y"]

    @property
    def lng(self):
        return self.point["x"]

    inscription_form = StreamField(
        [
            ('form_field', WagtailFormBlock(icon="form", label=_("Form field"))),
        ],
        use_json_field=True,
        blank=True,
        null=True,
        verbose_name=_("Inscription form"),
        help_text=_("Add an inscription form for this event."),
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('type'),
                FieldPanel("date"),
                FieldPanel("author"),
                FieldPanel("tags"),
            ],
            heading=_("Article informations"),
            classname="collapsible",
        ),
        FieldPanel("body", heading=_("Content"), classname="collapsible"),
        InlinePanel(
            "amicale_gallery",
            label=_("Image"),
            heading=_("Gallery"),
            classname="collapsible",
        ),
        FieldPanel("use_map"),
        MultiFieldPanel(
            [
                GeoAddressPanel(
                    "address", geocoder=geocoders.NOMINATIM, heading=_("Address")
                ),
                LeafletPanel(
                    "location",
                    address_field="address",
                    hide_latlng=True,
                    heading=_("Location"),
                ),
                FieldPanel("point_name", heading=_("Name (marker)")),
                FieldPanel("point_link", heading=_("Link (marker)")),
            ],
            heading=_("Map details"),
            classname="collapsible collapsed",
        ),
        FieldPanel("inscription_form", heading=_("inscription form"), classname="collapsible"),
    ]

    search_fields = Page.search_fields + [
        index.FilterField("date"),
        index.FilterField("type"),
        index.SearchField("body"),
        index.RelatedFields(
            "tags",
            [
                index.SearchField("name"),
                index.FilterField("name"),
            ],
        ),
        index.RelatedFields(
            "author",
            [
                index.SearchField("name"),
            ],
        ),
    ]

    api_fields = [
        APIField("body"),
    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

###############
##  WIDGETS  ##
############### 

# Auteurs
@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Author imge"),
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("author_image"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
    
# Galerie d'images
class AmicaleGallery(GalleryImage):
    """Modèle de carrousel d'images spécifique à la GenericPage."""
    page = ParentalKey(
        'AmicalePage',
        on_delete=models.CASCADE,
        related_name="amicale_gallery",
    )

# Tags
class AmicalePageTag(TaggedItemBase):
    content_object = ParentalKey(
        "AmicalePage",
        related_name=("tagged_items"),
        on_delete=models.CASCADE,
    )
