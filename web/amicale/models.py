from termcolor import colored

from django.db import models
from django.utils.timezone import datetime
from modelcluster.fields import ParentalKey

from wagtail import blocks
from wagtail.admin import messages
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

# Page de menu
from utils.menu_pages import MenuPage, menu_page_save

# Blocks, Medias, PJ, etc.
from utils.widgets import GalleryImage, PiecesJointes as PJBlock
from utils.nominatim import geocode

from utils.streamfield import (
    CustomParagraphBlock as ParagraphBlock,
    CustomImageBlock as ImageBlock,
    CustomTableBlock as TableBlock,
    CustomMediaBlock as MediaBlock,
    CustomEmbedBlock as EmbedBlock,
    CustomListBlock as ListBlock,
    CustomQuoteBlock as QuoteBlock,
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
    subpage_types = [
        "amicale.AmicalePage",
        "amicale.AmicaleInscriptionPage",
    ]
    save = menu_page_save("amicale")
    
    def get_context(self, request):
        context = super().get_context(request)
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

        user = request.user
        ami = False
        if user.is_authenticated and user.groups.filter(name='Amicale').exists():
            ami = True
                                
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
        context['ami'] = ami
        
        return context


#######################
## PAGE DE L'AMICALE ##
####################### 

# Page générique pour les articles (quel que soit le type)
class AmicalePage(Page):
    parent_page_types = ["amicale.AmicaleIndexPage"]
    subpage_types = []
    
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
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title", icon="title", label=_("Heading"))),
            ("paragraph", ParagraphBlock(icon="pilcrow", label=_("Paragraph"))),
            ("media", MediaBlock(icon="media", label=_("Media"))),            
            ("image", ImageBlock(icon="image", label=_("Image"))),
            ('document', DocumentChooserBlock(icon="doc-full-inverse", label=_("Document"))),            
            ("table", TableBlock(icon="table", label=_("Table"))),
            ("embed", EmbedBlock(icon="media", label=_("Embed media"))),
            ("list", ListBlock(icon="list-ul", label=_("List"))),
            ("quote", QuoteBlock(icon="openquote", label=_("Quote"))),
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

    form = StreamField(
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
        FieldPanel("form", heading=_("inscription form"), classname="collapsible"),
    ]

    search_fields = Page.search_fields + [
        index.FilterField("date"),
        index.FilterField("type"),
        index.SearchField("body"),
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

    def get_context(self, request, *args, **kwargs):        
        context = super().get_context(request, *args, **kwargs)
        home = request.GET.get('home', 'false') == 'true'
        user = request.user
        lat = None
        lng = None
        
        if self.use_map:
            a1 = user.address1
            a2 = user.address2
            zc = user.zip_code
            city = user.city
            
            lat, lng = geocode(a1, a2, zc, city, '')
              
            if home and (lat is None or lng is None):
                messages.warning(request, "Vous n'avez pas d'adresse définie dans votre profil. Cliquez sur la roue crantée pour la renseigner.")

        link = False
        if request.GET.get('inscription') == 'true':
            link = True 
     
        ami = False
        if user.is_authenticated and user.groups.filter(name='Amicale').exists():
            ami = True        

        context['ami'] = ami
        context['amicale_link'] = link
        context['user_lat'] = "{:.6f}".format(lat) if lat is not None else None
        context['user_lng'] = "{:.6f}".format(lng) if lng is not None else None
        return context

# Formulaire d'inscription à l'amicale
class AmicaleInscriptionPage(MenuPage):
    template = "amicale/formulaires/inscription.html"
    parent_page_types = ["amicale.AmicaleIndexPage"]
    subpage_types = []
    save = menu_page_save("inscription-amicale")
    
    introduction = RichTextField(
        blank=True,
        null=True,
        verbose_name=_("Introduction"),
        help_text=_("Here you can explain how the inscription works..."),
    )
    form = StreamField(
        [
            ('form_field', WagtailFormBlock(icon="form", label=_("Form field"))),
        ],
        use_json_field=True,
        blank=True,
        null=True,
        verbose_name=_("Inscription form"),
        help_text=_("The main form for the inscription to the amicale."),
        block_counts={
            'form_field': {'min_num': 1},
            'form_field': {'max_num': 1},
        },
    )
    
    # Panneau de contenu
    content_panels = MenuPage.content_panels + [
        FieldPanel("introduction", heading=_("Introduction"), classname="collapsible"),
        FieldPanel("form", heading=_("inscription form"), classname="collapsible"),
        InlinePanel(
            "inscription_documents",
            label=_("Document"),
            heading=_("Attachments"),
        ),
    ]
       

###############
##  WIDGETS  ##
############### 

# Galerie d'images
class AmicaleGallery(GalleryImage):
    """Modèle de carrousel d'images spécifique à la GenericPage."""
    page = ParentalKey(
        'AmicalePage',
        on_delete=models.CASCADE,
        related_name="amicale_gallery",
    )

# Liste de documents (GenericPage)
class AmicalePieceJointe(PJBlock):
    """Modèle de pièce jointe spécifique à la page d'inscription à l'amicale."""

    page = ParentalKey(
        AmicaleInscriptionPage,
        on_delete=models.CASCADE,
        related_name="inscription_documents",
    )
