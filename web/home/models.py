import io
import zipfile

from django.db import models
from django.conf import settings
from django.http import HttpResponse

from wagtail.models import Page

from wagtail.fields import (
    RichTextField, 
    StreamField,
    models
)
from wagtail.admin.panels import (
    FieldPanel, 
    MultiFieldPanel, 
    FieldRowPanel, 
    InlinePanel
)

# Blocks 
from wagtail.blocks import (
    CharBlock,
    RichTextBlock,
    ListBlock,
    BlockQuoteBlock,
)
from wagtail.images.blocks import ImageChooserBlock

# Blocks, Medias, PJ, etc.
from utils.widgets import GalleryImage, PiecesJointes as PJBlock
from utils.streamfield import (
    CustomMediaBlock as MediaBlock,
    CustomLinkBlock as LinkBlock,
    CustomEmbedBlock as EmbedBlock,
    CustomPDFBlock as PDFBlock,
    CustomDOCXBlock as DOCXBlock,
)

# Page de menu
from utils.menu_pages import MenuPage, menu_page_save

# Clefs
from modelcluster.fields import ParentalKey

# API
from wagtail.api import APIField

# Traduction
from django.utils.translation import gettext_lazy as _

# Recherche
from wagtail.search import index

# Formulaire
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

#####################
##  PAGES DU SITE  ##
##################### 

# Page d'accueil
class HomePage(MenuPage):
    parent_page_types = ['wagtailcore.Page']
    subpage_types = [
        'accompte.AccountPage',
        'administration.AdministrationIndexPage',
        'amicale.AmicaleIndexPage',
        'agents.FaqIndexPage',
        'joyous.CalendarPage',
        'home.RessourcesPage',
        'home.PublicPage',
    ]
    save = menu_page_save('accueil')

# Page générique
class GenericPage(Page):
    parent_page_types = ['home.RessourcesPage', 'home.PublicPage']	
    subpage_types = []
    show_in_menus_default = True
    max_count = None
    
    logo = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo (SVG, png, jpg, etc.)"),
        help_text=_("𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦: Round or square (1/1). 𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦𝐚𝐭: Filled SVG. 𝐒𝐞𝐜𝐨𝐧𝐝𝐚𝐫𝐲 𝐟𝐨𝐫𝐦𝐚𝐭: PNG with transparent background."),
    )
    heading = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Heading"),
        help_text=_("Displayed in menus, the heading is the title of the page."),
    )
    tooltip = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Tooltip"),
        help_text=_("Used for accessibility (alt, title) and when user mouse over the icon."),
    )    
    body = StreamField(
        [
            ("heading", CharBlock(classname="title", icon="title")),
            ("paragraph", RichTextBlock(icon="pilcrow")),
            ("media", MediaBlock(icon="media")),
            ("image", ImageChooserBlock(icon="image")),
            ("link", LinkBlock(icon="link")),
            ("embed", EmbedBlock(icon="media")),
            (
                "list",
                ListBlock(CharBlock(icon="radio-full"), icon="list-ul"),
            ),
            ("quote", BlockQuoteBlock(icon="openquote")),
        ],
        use_json_field=True,
        blank=True,
        null=True,
        verbose_name=_("Agenda"),
        help_text=_("This is the main content of the page."),
    )

    # Panneau de contenu
    content_panels = Page.content_panels + [
        MultiFieldPanel([
                FieldPanel("logo"),
                FieldPanel("heading"),
                FieldPanel("tooltip"),
            ],
            heading=_("Menu display options (click to expand)"),
            help_text=_("Choose an icon and a tooltip to display on the index pages. Both optional, if none, CGS logo will be the icon and tooltip will refer as the page title"),
            classname="collapsible, collapsed",
        ),
        FieldPanel("body", heading=_("Content")),
        InlinePanel(
            "generic_gallery",
            label=_("Image"),
            heading=_("Gallery"),
        ),
        InlinePanel(
            "generic_documents",
            label=_("Document"),
            heading=_("Attachments"),
        ),
    ]
    
    # Champs pour la recherche
    search_fields = Page.search_fields + [
        index.SearchField("heading"),
        index.SearchField("body"),
        index.RelatedFields('generic_documents', [
            index.SearchField('title'),
        ]),
    ]

    # Champs pour l'API
    api_fields = [
        APIField("heading"),
        APIField("body"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['menu_type'] = self.slug
        menu_pages = getattr(settings, "WAGTAIL_MENU_PAGES", [])        
        context['is_menu'] = self.__class__.__name__ in menu_pages
        return context
    
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

# Section page ressources diverses
class RessourcesPage(MenuPage):
    parent_page_types = ['home.HomePage']
    subpage_types = [
        'home.GenericPage',
        'home.InstantDownloadPage',
        'home.FormPage',
    ]
    save = menu_page_save('ressources')

    def get_context(self, request):
        context = super().get_context(request)
        grouped_subpages, search_query, page_type = generic_search(request, self)
        
        context['grouped_subpages'] = grouped_subpages
        context['search_query'] = search_query
        context['type'] = page_type
        return context

# Section pages publiques
class PublicPage(MenuPage):
    parent_page_types = ['home.HomePage']
    subpage_types = [
        'home.GenericPage',
        'home.InstantDownloadPage',
        'home.FormPage',
    ]
    save = menu_page_save('public')

    def get_context(self, request):
        context = super().get_context(request)
        grouped_subpages, search_query, page_type = generic_search(request, self)
        
        context['grouped_subpages'] = grouped_subpages
        context['search_query'] = search_query
        context['type'] = page_type
        return context

# Page pour document à télécharger
class InstantDownloadPage(MenuPage):
    parent_page_types = ['home.RessourcesPage', 'home.PublicPage']
    subbpage_types = []
    max_count = None
            
    # Panneau de contenu
    content_panels = MenuPage.content_panels + [
        InlinePanel(
            "download_documents",
            min_num=1,
            max_num=10,
            label=_("Document"),
            heading=_("Attachments"),
            help_text=_("Add one or more documents to download. If multiple documents are added, they will be downloaded as a zip file. Icon and Tooltip are optional, if none, icon will be generic image and tooltip will be the page title."),
        ),
    ]
    
    # Champs pour la recherche
    search_fields = Page.search_fields + [
        index.SearchField("heading"),
        index.RelatedFields('download_documents', [
            index.AutocompleteField('title'),
        ]),
    ]

    # Champs pour l'API
    api_fields = [
        APIField("heading"),
        APIField("intro"),
    ]
    
    def serve(self, request):
        # Récupère tous les objets InstantDownloadPieceJointe liés à cette page
        attachments = self.download_documents.all()

        # Si un seul document est associé
        if len(attachments) == 1:
            document = attachments[0].document
            response = HttpResponse(document.file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
            return response

        # Si plusieurs documents sont associés
        elif len(attachments) > 1:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                for attachment in attachments:
                    document = attachment.document
                    zip_file.writestr(document.filename, document.file.read())
            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="documents.zip"'
            return response

        # Si aucun document n'est associé, affichez la page normalement
        return super().serve(request)
    
    def save(self, *args, **kwargs):
        if not self.title:  # Si le titre n'est pas déjà défini
            self.title = "Téléchargement instantané"
        if not self.slug:  # Si le slug n'est pas déjà défini
            self.slug = "dlslug"
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = _("Instant download page")
        verbose_name_plural = _("Instant download pages")

# Formulaire d'inscription 2/2 (Page)
class FormPage(AbstractEmailForm):
    parent_page_types = ['home.RessourcesPage', 'home.PublicPage']
    subpage_types = []
    
    logo = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo (SVG, png, jpg, etc.)"),
        help_text=_("𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦: Round or square (1/1). 𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦𝐚𝐭: Filled SVG. 𝐒𝐞𝐜𝐨𝐧𝐝𝐚𝐫𝐲 𝐟𝐨𝐫𝐦𝐚𝐭: PNG with transparent background."),
    )
    heading = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Heading"),
        help_text=_("Displayed in menus, the heading is the title of the page."),
    )
    tooltip = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Tooltip"),
        help_text=_("Used for accessibility (alt, title) and when user mouse over the icon."),
    )    
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel([
                FieldPanel("logo"),
                FieldPanel("heading"),
                FieldPanel("tooltip"),
            ],
            heading=_("Menu display options (click to expand)"),
            help_text=_("Choose an icon and a tooltip to display on the index pages. Both optional, if none, CGS logo will be the icon and tooltip will refer as the page title"),
            classname="collapsible, collapsed",
        ),
        FieldPanel('intro'),        
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
    
    # Champs pour la recherche
    search_fields = Page.search_fields + [
        index.SearchField("heading"),
        index.SearchField("intro"),
    ]

    # Champs pour l'API
    api_fields = [
        APIField("heading"),
        APIField("intro"),
    ]

###############
##  WIDGETS  ##
############### 

class GenericGallery(GalleryImage):
    """Modèle de carrousel d'images spécifique à la GenericPage."""
    page = ParentalKey(
        GenericPage,
        on_delete=models.CASCADE,
        related_name="generic_gallery",
    )

# Liste de documents (GenericPage)
class GenericPieceJointe(PJBlock):
    """Modèle de pièce jointe spécifique à la CompteRenduPage."""

    page = ParentalKey(
        GenericPage,
        on_delete=models.CASCADE,
        related_name="generic_documents",
    )
  
# Liste de documents (GenericPage)
class InstantDownloadPieceJointe(PJBlock):
    """Modèle de pièce jointe spécifique à la CompteRenduPage."""

    page = ParentalKey(
        InstantDownloadPage,
        on_delete=models.CASCADE,
        related_name="download_documents",
    )
    
# Formulaire d'inscription (abstract form field)
class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

###############
## FONCTIONS ##
############### 

# Recherche générique (RessourcesPage, PublicPage)
def generic_search(request, parent_page):
    search_query = request.GET.get('query', '')
    page_type = request.GET.get('type', 'all')

    # On récupère toutes les sous-pages
    subpages = Page.objects.child_of(parent_page).specific()

    # On applique le filtrage par type
    if page_type != 'all':
        filtered_subpages = []
        for subpage in subpages:
            if page_type == 'generic' and isinstance(subpage, GenericPage):
                filtered_subpages.append(subpage)
            elif page_type == 'download' and isinstance(subpage, InstantDownloadPage):
                filtered_subpages.append(subpage)
            elif page_type == 'form' and isinstance(subpage, FormPage):
                filtered_subpages.append(subpage)
        subpages = filtered_subpages

    # On applique la query
    if search_query:
        subpages = [subpage for subpage in subpages if search_query.lower() in subpage.title.lower()]

    # On groupe les sous-pages par type
    grouped_subpages = {
        'generic': [sp for sp in subpages if isinstance(sp, GenericPage)],
        'download': [sp for sp in subpages if isinstance(sp, InstantDownloadPage)],
        'form': [sp for sp in subpages if isinstance(sp, FormPage)],
    }
        
    return grouped_subpages, search_query, page_type
