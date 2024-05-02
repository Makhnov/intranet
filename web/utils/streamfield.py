import re
from django.conf import settings
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
    RichTextBlock,
    BlockQuoteBlock,
)

# Images
from wagtail.images.blocks import ImageChooserBlock
from images.models import CustomImage
from pdf2image import convert_from_bytes

# Tableaux
from wagtail.contrib.table_block.blocks import TableBlock

# UTILS
from utils.variables import STOP_WORDS
from utils.variables import STOP_WORDS, TABLE_OPTIONS

# IMPORTS
from utils.imports import (
    save_wagtail_image, 
    get_collections, 
    get_docx_content,
)

# API
from wagtail.api import APIField

# Traduction
from django.utils.translation import gettext_lazy as _

# Recherche
from wagtail.search import index

#############################################################################################################
#                                 Blocs dans les streamfields et streamblocks                               #
#              Le StreamBlock est un élément du body (StreamField) des pages de certaines pages             #
#                                     Amicale, compte-rendus, génériques                                    #
#############################################################################################################

# Positionnement pour certains éléments d'un streamfield/streamblock à gauche, au centre, à droite ou justifiés
class PositionBlock(ChoiceBlock):
    choices = [
        ("left", _("Left")),
        ("center", _("Center")),
        ("right", _("Right")),
        ("justify", _("Justify")),
    ]
    label = _("alignement")
    class Meta:
        icon = "placeholder"

# Taille pour certains éléments d'un streamfield/streamblock peuvent être de taille icon, small, medium, large ou full
class SizeBlock(ChoiceBlock):
    choices = [
        ("icon", _("Icon")),
        ("small", _("Small")),
        ("medium", _("Medium")),
        ("large", _("Large")),
        ("full", _("Full")),
    ]
    label = _("size")
    class Meta:
        icon = "placeholder"

# Liste de choix pour sélectionner les couleurs du thème CGS
class ColorBlock(ChoiceBlock):
    choices = [
        ("green", _("Green")),
        ("darkgreen", _("Dark Green")),
        ("cyan", _("Cyan")),
        ("lightgreen", _("Vert d'eau")),
        ("orange", _("Orange")),
    ]
    
# Liste personnalisée
class CustomListBlock(StructBlock):
    list = ListBlock(
        CharBlock(
            required=True,
            label=_("Item"),
            icon="radio-full",
        ),
        label=_("List"),
        icon="list-ul",
    )
    position = PositionBlock(
        required=False,
        default="justify"
    )
    size = SizeBlock(
        required=False,
        default="medium",
    )
    
    class Meta:
        icon = "list-ul"
        label = _("List")

# Citation personnalisée
class CustomQuoteBlock(StructBlock):
    quote = BlockQuoteBlock(
        required=True,
        label=_("Quote"),
    )
    author = CharBlock(
        required=False,
        label=_("Author"),
    )
    position = PositionBlock(
        required=False,
        default="center",
    )
    size = SizeBlock(
        required=False,
        default="medium",
    )
    class Meta:
        icon = "openquote"
        label = _("Quote")
        
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
    position = PositionBlock(
        required=False,
        default="center",
    )
    size = SizeBlock(
        required=False,
        default="medium",
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
class CustomMediaBlock(StructBlock):
    media = AbstractMediaChooserBlock(required=True, help_text=_("Choose a media item"))
    position = PositionBlock(
        required=False,
        default="center",
    )
    size = ChoiceBlock(
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
        icon = 'media'
        label = _('Media')
        
# Bloc bouton
class CustomButtonBlock(StructBlock):
    url = URLBlock(
        required=True,
        label=_("URL"),
        help_text=_("Enter the URL."),
    )
    text = CharBlock(
        required=False,
        label=_("Button text"),
        help_text=_("Enter the visible text for this link (optional)."),
    )
    position =  PositionBlock(
        required=False,
        default="center",
    )
    color = ColorBlock(
        required=False,
        default="green",
        help_text=_("Optionnal, default is green."),
    )
    icon = ImageChooserBlock(
        required=False,
        icon="image", 
        label=_("Button image"),
        help_text=_("Optionnal"),
    )

    class Meta:
        icon = "button"
        label = _("Button")
        form_classname = "button-block"

# Bloc de document
class CustomDocumentBlock(StructBlock):
    document = DocumentChooserBlock(
        required=True,
        label=_("Document"),
        help_text=_("Choose a document to display."),
    )
    text = CharBlock(
        required=False,
        label=_("Text"),
        help_text=_("Enter the visible text for this document (optional)."),
    )
    position = PositionBlock(
        required=False,
        default="center",
    )
    color = ColorBlock(
        required=False,
        default="green",
        help_text=_("Optionnal, default is green. The icon will be add automatically (extension of the document)."),
    )
    class Meta:
        icon = "doc-full-inverse"
        label = _("Document")    
       
# Les titres de niveau 1 à 6      
class CustomHeadingBlock(StructBlock):
    heading = CharBlock(
        required=True,
        label=_("content"),
    )
    heading_level = ChoiceBlock(
        choices=[
            ("h1", _("Heading 1")),
            ("h2", _("Heading 2")),
            ("h3", _("Heading 3")),
            ("h4", _("Heading 4")),
            ("h5", _("Heading 5")),
            ("h6", _("Heading 6")),
        ],
        required=False,
        default="h2",
        label=_("level"),
    )
    position = PositionBlock(
        required=False,
        default="center",
    )    
    class Meta:
        icon = "title"
        label = _("Heading")
        abstract = True
        
# Les paragraphes
class CustomParagraphBlock(StructBlock):
    paragraph = RichTextBlock(
        required=True,
        label=_("content"),
    )
    position = PositionBlock(
        required=False,
        default="justify",
    )    
    class Meta:
        icon = "pilcrow"
        label = _("Paragraph")
        abstract = True
    
# Les images
class CustomImageBlock(StructBlock):
    image = ImageChooserBlock(
        required=True,
        label=_("content"),
    )
    position = PositionBlock(
        required=False,
        default="center",
    )
    size = SizeBlock(
        required=False,
        default="large",
    )
    class Meta:
        icon = "image"
        label = _("Image")
        abstract = True

# Les tableaux
class CustomTableBlock(StructBlock):
    table = TableBlock(
        required=True,
        label=_("content"),
        table_options=TABLE_OPTIONS,
    )
    position = PositionBlock(
        required=False,
        default="center",
    )
    size = SizeBlock(
        required=False,
    )
    class Meta:
        icon = "table"
        label = _("Table")

#############################################################################################################
#                                   Streamblocks Compte-rendus PDF et DOCX                                  #
#############################################################################################################

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
            ("heading", CustomHeadingBlock()),
            ("paragraph", CustomParagraphBlock()),
            ("image", CustomImageBlock()),
            ("table", CustomTableBlock()),
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
        template = "widgets/blocks/fields/PDF.html"
