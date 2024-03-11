import re
from django.conf import settings
from django.utils.html import format_html
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from wagtail.models import Page

from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import AbstractMediaChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

from wagtail.blocks import (
    StreamBlock, 
    StructBlock, 
    CharBlock, 
    ChoiceBlock,
    ListBlock, 
    URLBlock, 
    BooleanBlock,
)

# Images
from images.models import CustomImage
from pdf2image import convert_from_bytes

# Medias
from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join

# UTILS
from utils.variables import STOP_WORDS

# IMPORTS
from utils.imports import (
    save_wagtail_image, 
    get_collections, 
    get_docx_content, 
    HeadingDOCXBlock, 
    ParagraphDOCXBlock, 
    TableDOCXBlock, 
    ImageDOCXBlock,
)

# API
from wagtail.api import APIField

# Traduction
from django.utils.translation import gettext_lazy as _

# Recherche
from wagtail.search import index

#####################
##  BLOCS CUSTOMS  ##
##################### 

# Import de fichiers docx intégrée dans CompteRenduPage (package : mammoth)
class CustomDOCXBlock(StructBlock):
    docx_document = DocumentChooserBlock(
        required=True,
        label=_("Document"),
        help_text=_("Chose a DOCX file to import in the flow."),
    )
    docx_import = BooleanBlock(
        required=False,
        default=False,
        label=_("Save and import"),
        help_text=_("Use cautiously. It will override all existing content in this section."),
    )
    docx_content = StreamBlock(
        [
            ("heading", HeadingDOCXBlock()),
            ("paragraph", ParagraphDOCXBlock()),
            ("image", ImageDOCXBlock()),
            ("table", TableDOCXBlock()),
        ], 
        required=False, 
        classname="collapsible, collapsed", 
        label=_("Aperçu du contenu"),
        help_text=_("You can remove or replace any of the content below. If you want to restore the original content, click again on the import button."),
    )

    # Champs pour la recherche
    search_fields = Page.search_fields + [
        index.FilterField("docx_document"),
        index.RelatedField("docx_content", [
            index.RelatedField("heading" , [
                index.SearchField("heading"),
            ]),
            index.RelatedField("paragraph" , [
                index.SearchField("paragraph"),
            ]),
            index.RelatedField("image" , [
                index.FilterField("image"),
            ]),
            index.RelatedField("table" , [
                index.FilterField("table"),
            ]),
        ]),
    ]
    
    # Champs pour l'API
    api_fields = [
        APIField("docx_document"),
        APIField("content"),
    ]
    
    def clean(self, value):
        cleaned_data = super().clean(value)
        docx_document = cleaned_data.get('docx_document')

        if docx_document:  # Vérifie s'il y a un document sélectionné
            # Vérifie l'extension du fichier
            if not docx_document.filename.lower().endswith('.docx'):
                raise ValidationError({
                    'docx_document': ValidationError(
                        _("The file '%(filename)s' is not a DOCX document."),
                        params={'filename': docx_document.filename},
                        code='invalid',
                    )
                })
                
        return cleaned_data
    
    def get_content(self, document, collection_date, collection_restrictions):    
        image_title = "DOCX Image"
        image_tags = ["docx", "compte-rendu"]      
        collection_name = slugify(document.title)        
        # On récupère le premier mot "significatif" du document pour son titre et ajouter le tag
        words = re.split('-|_', collection_name)
        for word in words:
            if word not in STOP_WORDS and word != "":
                image_title = word.capitalize()
                if word.lower() not in image_tags:
                    image_tags.append(word)
                break
            
        document_collection = get_collections(collection_date, collection_name, collection_restrictions)   
          
        # Vérifiez si les images existent déjà avant de les créer dans la sous-collection spécifique
        existing_images = CustomImage.objects.filter(collection=document_collection)
        if existing_images.exists():
            existing_images.delete()
            
        return get_docx_content(document, image_title, image_tags, document_collection)
    
# Import de PDF intégrée dans CompteRenduPage (package : pdf2image)
class CustomPDFBlock(StructBlock):
    pdf_document = DocumentChooserBlock(
        required=True,
        label=_("Document"),
        help_text=_("Chose a PDF wich will be converted to images and added in the flow. Name smartly the document, it will be used to create a collection."),
    )
    pdf_import = BooleanBlock( 
        required=False,
        default=False,
        label=_("Save and import"),
        help_text=_("Use cautiously. It will override all existing images in this section."),
    )
    pdf_images = ListBlock(
        ImageChooserBlock(
            required=False,
        ), 
        required=False,
        classname="collapsible, collapsed",
        label=_("Aperçu des pages"),
        help_text=_("You can remove or replace any of the images below. If you want to restore the original images, click again on the import button."),
    )

    # Champs pour la recherche
    search_fields = Page.search_fields + [
        index.FilterField("pdf_document"),
        index.FilterField("pdf_images"),
    ]

    # Champs pour l'API
    api_fields = [
        APIField("pdf_document"),
        APIField("pdf_images"),
    ]
    
    def clean(self, value):
        cleaned_data = super().clean(value)
        pdf_document = cleaned_data.get('pdf_document')

        if pdf_document:  # Vérifie s'il y a un document sélectionné
            # Vérifie l'extension du fichier
            if not pdf_document.filename.lower().endswith('.pdf'):
                raise ValidationError({
                    'pdf_document': ValidationError(
                        _("The file '%(filename)s' is not a PDF document."),
                        params={'filename': pdf_document.filename},
                        code='invalid',
                    )
                })

        return cleaned_data
            
    def get_content(self, document, collection_date, collection_restrictions):    
        # Initialisation des variables
        image_title = "PDF Image"
        image_tags = ["pdf", "compte-rendu"]
        image_ids = []           
        
        collection_name = slugify(document.title)

        # On récupère le premier mot "significatif" du document pour son titre
        words = re.split('-|_', collection_name)
        for word in words:
            if word not in STOP_WORDS and word != "":
                image_title = word.capitalize()
                image_tags.append(word)
                break        
        
        document_collection = get_collections(collection_date, collection_name, collection_restrictions)
                        
        # Convertir le PDF en images 
        poppler_path = settings.POPPLER_PATH
        pdf_data = document.file.read()
        pdf_images = convert_from_bytes(pdf_data, fmt="jpeg", poppler_path=poppler_path)
            
        # Vérifiez si les images existent déjà avant de les créer dans la sous-collection spécifique
        existing_images = CustomImage.objects.filter(collection=document_collection)
        if existing_images.exists():
            existing_images.delete()
        
        for i, image in enumerate(pdf_images):
            image_id = save_wagtail_image(image, i, "jpeg", image_title, image_tags, document_collection, "pdf")
            image_ids.append(image_id)
            
        return image_ids

    class Meta:
        label = _("PDF")
        template = "widgets/blocks/PDF_block.html"

# Lien personnalisé
class CustomLinkBlock(StructBlock):
    url = URLBlock(label=_("URL"), help_text=_("Enter the URL."))
    text = CharBlock(
        required=False,  # Ceci rend le champ optionnel
        label=_("Replacement Text"),
        help_text=_("Enter the visible text for this link (optional)."),
    )

    class Meta:
        icon = "link"
        label = _("Link")

# Embed bloc personnalisé
class CustomEmbedBlock(StructBlock):
    embed_url = EmbedBlock(label=_("URL a intégrer"))
    resolution = ChoiceBlock(
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
    alternative_title = CharBlock(
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
class CustomMediaBlock(AbstractMediaChooserBlock):
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
