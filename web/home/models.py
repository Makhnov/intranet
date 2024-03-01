from termcolor import colored
import zipfile
import re
import io
from io import BytesIO

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.http import HttpResponse
from django.core.files.base import ContentFile

from wagtail import blocks
from wagtail.blocks import StreamBlock
from wagtailcharts.blocks import ChartBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.models import Page, Orderable, Collection
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel

# Page de menu
from utils.menu_pages import MenuPage, menu_page_save

# Documents
from wagtail.documents.models import Document

# Images
from images.models import CustomImage
from pdf2image import convert_from_bytes

# Wagtail Media
from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join
from wagtailmedia.blocks import AbstractMediaChooserBlock

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

# Charts
from utils.variables import CHART_COLORS, CHART_TYPES, STOP_WORDS


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


# PDF => images
class CustomPDFBlock(blocks.StructBlock):

    heading = blocks.CharBlock(
        required=False, 
        blank=True,
        label=_("Heading"),
        help_text=_("Automatically generated if left blank. This is the title of the PDF."),
    )
    document = DocumentChooserBlock(
        required=True,
        label=_("Document"),
        help_text=_("Chose a PDF wich will be converted to images and added in the flow."),
    )
    images = blocks.ListBlock(
        ImageChooserBlock(
            required=False,
            read_only=True,
        ), 
        required=False,
        label=_("Aperçu des pages"),
        help_text=_("You can remove or replace any of the images below. If you want to restore the original images, you must delete the block and add it again."),
    )
    # Panneau de contenu
    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        FieldPanel("document"),
        FieldPanel("images"),
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
    
    def get_pdf_images(self, document):                
        pdf_data = document.file.read()
        pdf_images = convert_from_bytes(pdf_data, fmt="jpeg", poppler_path=r"C:\\Program Files\\poppler-24.02.0\\Library\\bin")
        
        # On slugify le titre du document pour le nom de la collection
        collection_name = slugify(document.title)
        root_collection = Collection.objects.get(name="PDF")

        # On récupère le premier mot "significatif" du document pour son titre
        words = re.split('-|_', collection_name)
        image_title = "PDF Image"
        for word in words:
            if word not in STOP_WORDS and word != "":
                image_title = word.capitalize()
                break
    
        # On crée la collection si elle n'existe pas
        try:
            collection = root_collection.get_children().get(name=collection_name)
        except Collection.DoesNotExist:
            collection = root_collection.add_child(name=collection_name)

        # Vérifiez si les images existent déjà avant de les créer
        existing_images = CustomImage.objects.filter(collection__name=collection_name)
        # print(existing_images)
        if existing_images.exists():
            # Supprimez les images existantes si vous voulez les remplacer par de nouvelles
            existing_images.delete()
        
        image_ids = []
        for i, image in enumerate(pdf_images):
            # Convertir l'image PIL en bytes
            img_bytes = BytesIO()
            image.save(img_bytes, format='JPEG')
            img_bytes = img_bytes.getvalue()

            # Créer l'instance de CustomImage
            wagtail_image = CustomImage(file=ContentFile(img_bytes, name=f"pdf_image_{i}.jpeg"), title=f"{image_title} {i}", collection=collection)
            wagtail_image.save()
            image_ids.append(wagtail_image.id)
            
        # print(image_ids)
        return image_ids

    
    class Meta:
        label = _("PDF")
        template = "widgets/blocks/PDF_block.html"


# Charts
class CustomChartBlock(StreamBlock):
    chart_block = ChartBlock(colors=CHART_COLORS, chart_type=CHART_TYPES)


# Lien personnalisé
class CustomLinkBlock(blocks.StructBlock):
    url = blocks.URLBlock(label=_("URL"), help_text=_("Enter the URL."))
    text = blocks.CharBlock(
        required=False,  # Ceci rend le champ optionnel
        label=_("Replacement Text"),
        help_text=_("Enter the visible text for this link (optional)."),
    )

    class Meta:
        icon = "link"
        label = _("Link")


# Embed bloc personnalisé
class CustomEmbedBlock(blocks.StructBlock):
    embed_url = EmbedBlock(label=_("URL a intégrer"))
    resolution = blocks.ChoiceBlock(
        choices=[
            ("very_small", _("Very small")),
            ("small", _("Small")),
            ("medium", _("Medium")),
            ("large", _("Large")),
            ("very_large", _("Very large")),
        ],
        default="medium",
        label=_("Size of the frame"),
    )
    alternative_title = blocks.CharBlock(
        blank=True,
        required=False,
        label=_("Alternative title"),
        help_text=_("Alternative title for users accessibility."),
    )

    class Meta:
        template = "widgets/images/embed_block.html"
        icon = "media"
        label = _("Intégration vidéo")


# Bloc media
class MediaBlock(AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        if not value:
            return ""

        if value.type == "video":
            player_code = _(
                """
            <div>
                <video width="{1}" height="{2}" controls>
                    {0}
                    Your browser does not support the video tag.
                </video>
            </div>
            """
            )
        else:
            player_code = _(
                """
            <div>
                <audio controls>
                    {0}
                    Your browser does not support the audio element.
                </audio>
            </div>
            """
            )

        return format_html(
            player_code,
            format_html_join(
                "\n", "<source{0}>", [[flatatt(s)] for s in value.sources]
            ),
            value.width,
            value.height,
        )


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
            ("heading", blocks.CharBlock(classname="title", icon="title")),
            ("paragraph", blocks.RichTextBlock(icon="pilcrow")),
            ("media", MediaBlock(icon="media")),
            ("image", ImageChooserBlock(icon="image")),
            ("link", CustomLinkBlock(icon="link")),
            ("embed", EmbedBlock(icon="media")),
            (
                "list",
                blocks.ListBlock(blocks.CharBlock(icon="radio-full"), icon="list-ul"),
            ),
            ("quote", blocks.BlockQuoteBlock(icon="openquote")),
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
            "gallery_images",
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

  
# Formulaire d'inscription 1/2 (champs personnalisés)
class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

      
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


# Carrousel d'image (HomePage)
class HomePageGalleryImage(Orderable):
    page = ParentalKey(
        GenericPage,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ForeignKey(
        "images.CustomImage",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="",
    )
    caption = models.CharField(
        blank=True,
        max_length=250,
        verbose_name=_("Caption"),
        help_text=_("You can add a caption to the image (optional)."),
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]


# Pièces Jointes
class PiecesJointes(Orderable):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("File"),
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=250,
        verbose_name=_("Title"),
        null=True,
        blank=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("document"),
                FieldPanel("title"),
            ]
        )
    ]

    class Meta:
        abstract = True
        

# Liste de documents (GenericPage)
class GenericPieceJointe(PiecesJointes):
    """Modèle de pièce jointe spécifique à la CompteRenduPage."""

    page = ParentalKey(
        GenericPage,
        on_delete=models.CASCADE,
        related_name="generic_documents",
    )

  
# Liste de documents (GenericPage)
class InstantDownloadPieceJointe(PiecesJointes):
    """Modèle de pièce jointe spécifique à la CompteRenduPage."""

    page = ParentalKey(
        InstantDownloadPage,
        on_delete=models.CASCADE,
        related_name="download_documents",
    )
