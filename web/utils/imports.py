
import base64
from io import BytesIO
from PIL import Image

import logging
logger = logging.getLogger(__name__)
from PIL import UnidentifiedImageError
from termcolor import colored

import mammoth
from bs4 import BeautifulSoup, element

from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.blocks import CharBlock, ChoiceBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock

from images.models import CustomImage
from utils.variables import STOP_WORDS, TABLE_OPTIONS
from wagtail.models import (
    Collection, 
    CollectionViewRestriction,
)

#############################################################################################################
#                                   Blocs dans le StreamBlock (docx_content)                                #
#               Le StreamBlock est un élément du body (StreamField) des pages de compte-rendu               #
#                   Pour les utilisateurs qui souhaitent importer un document Word (docx)                   #
#############################################################################################################

# Tous les éléments importés peuvent être positionnés à gauche, au centre, à droite ou justifiés
class PositionBlock(blocks.ChoiceBlock):
    choices = [
        ("left", _("Left")),
        ("center", _("Center")),
        ("right", _("Right")),
        ("justify", _("Justify")),
    ]
    label = _("alignement")
    class Meta:
        icon = "placeholder"

# Les titres de niveau 1 à 6      
class HeadingDOCXBlock(blocks.StructBlock):
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
class ParagraphDOCXBlock(blocks.StructBlock):
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
class ImageDOCXBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=True,
        label=_("content"),
    )
    position = PositionBlock(
        required=False,
        default="center",
    )
    size = ChoiceBlock(
        choices=[
            ("icon", _("Icon")),
            ("small", _("Small")),
            ("medium", _("Medium")),
            ("large", _("Large")),
            ("full", _("Full")),
        ],
        required=False,
        default="large",
        label=_("size"),
    )    
    class Meta:
        icon = "image"
        label = _("Image")
        abstract = True

# Les tableaux
class TableDOCXBlock(blocks.StructBlock):
    table = TableBlock(
        required=True,
        label=_("content"),
        table_options=TABLE_OPTIONS,
    )
    position = PositionBlock(
        required=False,
        default="center",
    )    
    class Meta:
        icon = "table"
        label = _("Table")
        abstract = True

# Gestion des collections 
def get_collections(collection_date, collection_name, collection_restrictions):   
    
    # On récupère la collection racine ("ROOT") 
    root_collection = Collection.objects.get(name="Root")    
    print(root_collection)
    
    # On récupère, ou on créé la collection "PDF"
    try:
        pdf_collection = root_collection.get_children().get(name="PDF")
    except Collection.DoesNotExist:
        pdf_collection = root_collection.add_child(name="PDF")
    print(pdf_collection)
    
    def apply_restrictions(collection, restrictions):
        for restriction in restrictions:
            view_restrictions = CollectionViewRestriction.objects.create(
                collection=collection,
                restriction_type=restriction.restriction_type,
                password=restriction.password,
            )
            # Ajout des restrictions de groupe
            for group in restriction.groups.all():
                view_restrictions.groups.add(group)
          
    # On récupère, ou on créé la collection qui regroupe tous les documents associé au compte-rendu en cours      
    try:
        cr_collection = pdf_collection.get_children().get(name=collection_date)
    except Collection.DoesNotExist:
        cr_collection = pdf_collection.add_child(name=collection_date)
        apply_restrictions(cr_collection, collection_restrictions)
    print(cr_collection)
      
    # On récupère, ou on créé la collection qui regroupe toutes les images du document en cours  
    try:
        document_collection = cr_collection.get_children().get(name=collection_name)
    except Collection.DoesNotExist:
        document_collection = cr_collection.add_child(name=collection_name)
        # apply_restrictions(document_collection, collection_restrictions)
        
    return document_collection

# Conversion du document Word en html
def get_docx_content(document, image_title, image_tags, document_collection):
    with document.file.open('rb') as docx_file:
        style_map = "p[style-name='Aside Text'] => p.aside-text:fresh"
        result = mammoth.convert_to_html(docx_file, style_map=style_map)
        content = result.value
        soup = BeautifulSoup(content, 'html.parser')
        content_blocks = get_soup_content(soup, image_title, image_tags, document_collection)        
        
        # Filtrer les blocs 
        filtered_blocks = []
        for typ, blk in content_blocks:
            if not (isinstance(blk, str) and not blk.strip()):
                # Ajoute ce bloc si blk n'est pas une chaîne vide
                filtered_blocks.append((typ, blk))
        return filtered_blocks
          
# Tri des résultats du parsing BS4
def get_soup_content(soup, image_title, image_tags, document_collection, parent_type=None):
    blocks = []
    paragraph_buffer = []
    image_index=0
    
    def flush_paragraph_buffer():
        non_empty_paragraphs = [p for p in paragraph_buffer if p.strip()]
        if non_empty_paragraphs:
            merged_paragraphs = ''.join(non_empty_paragraphs)
            blocks.append(('paragraph', merged_paragraphs))
        paragraph_buffer.clear()
    
    for child in soup.children:
        if isinstance(child, element.Tag):
            if child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                flush_paragraph_buffer()
                if child.get_text(strip=True):  # Vérifier si le titre contient du texte
                    blocks.append(('heading', (child.name, child.get_text(strip=True))))
            elif child.name == 'p':
                if parent_type == 'table':  # Ignorer les paragraphes à l'intérieur des tables
                    continue
                else:
                    image = child.find(['img', 'svg', 'iframe', 'canvas'])
                    if image:                        
                        flush_paragraph_buffer()  # Traiter le texte du paragraphe s'il existe
                        if child.get_text(strip=True):  # Si le paragraphe contient du texte
                            paragraph_text = str(child)
                            paragraph_text = paragraph_text.replace(str(image), "")  # Retirer l'image du paragraphe
                            blocks.append(('paragraph', paragraph_text))
                        wagtail_image = convert_image(image, image_index, image_title, image_tags, document_collection)
                        if wagtail_image is not None:
                            blocks.append(('image', wagtail_image))
                            image_index += 1
                    else:
                        paragraph_buffer.append(str(child))
            elif child.name == 'table':
                flush_paragraph_buffer()
                table = convert_table(table_html=str(child))
                blocks.append(('table', table))
            elif child.name in ['img', 'svg', 'iframe', 'canvas'] and not parent_type:
                flush_paragraph_buffer()
                wagtail_child_image = convert_image(image, image_index, image_title, image_tags, document_collection)
                if wagtail_child_image is not None:
                    blocks.append(('image', wagtail_child_image))
                    image_index += 1
            else:
                flush_paragraph_buffer()
                blocks.extend(get_soup_content(child, image_title, image_tags, document_collection, parent_type=child.name))
        elif isinstance(child, element.NavigableString) and parent_type != 'table' and child.strip():
            paragraph_buffer.append(str(child))

    flush_paragraph_buffer()  # On vide le buffer à la fin
    return blocks

# Gestion des tables
def convert_table(table_html):
    soup = BeautifulSoup(table_html, 'html.parser')
    rows = soup.find_all('tr')
    data = []
    first_row_is_table_header = False
    first_col_is_header = False

    # Parcourir chaque ligne pour extraire les données
    for row_index, row in enumerate(rows):
        row_data = []
        cells = row.find_all(['td', 'th'])

        for cell_index, cell in enumerate(cells):
            cell_text = ' '.join(cell.stripped_strings)
            # Ignorer la cellule en haut à gauche pour cette évaluation
            if row_index == 0 and cell_index == 0:
                caption = cell_text
                row_data.append(cell_text)
                continue

            # Déterminer les en-têtes de ligne et de colonne
            if cell.find('strong') is not None:
                if cell_index == 0:
                    first_col_is_header = True
                if row_index == 0:
                    first_row_is_table_header = True

            row_data.append(cell_text)

        data.append(row_data)

    # Déduire table_header_choice
    if first_col_is_header and first_row_is_table_header:
        table_header_choice = 'both'
    elif first_col_is_header:
        table_header_choice = 'column'
    elif first_row_is_table_header:
        table_header_choice = 'row'
    else:
        table_header_choice = 'neither'

    # Créer la structure de données finale pour Wagtail
    table_structure = {
        'cell': [],  # Informations sur les cellules, si nécessaire
        'data': data,
        'mergeCells': [],  # Gérer les cellules fusionnées, si nécessaire
        'table_caption': caption,  # Ajouter une légende si nécessaire
        'first_col_is_header': first_col_is_header,
        'first_row_is_table_header': first_row_is_table_header,
        'table_header_choice': table_header_choice,
    }
    return table_structure

# Gestion des images
def convert_image(image, image_index, image_title, image_tags, document_collection):
    try:
        # Si l'image a un attribut "title" on l'utilise
        if image.get('title'):
            image_title = image.get('title')
        
        # Construction de l'instance de CustomImage
        src = image['src']
        
        # Extraire les données en base64 (supposer que le format est "data:image/png;base64,...")
        header, base64_data = src.split(',', 1)
        image_format = header.split(';')[0].split('/')[1]  # Exemple: 'image/png' -> 'png'

        # Décoder l'image en base64
        image_bytes = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_bytes))    
        
        # La fonction de création d'image nous renvoie l'ID de l'image créée
        return save_wagtail_image(image, image_index, image_format, image_title, image_tags, document_collection, "docx")
    except Exception as e:
        logger.error(f"Erreur lors de la conversion de l'image {image_index}: {e}")
        return None   
            
# Enregistrement des images dans Wagtail
def save_wagtail_image(image, image_index, image_format, image_title, image_tags, document_collection, document_type):
    try:
        # Convertir l'image PIL en bytes
        img_bytes = BytesIO()
        image.save(img_bytes, format=image_format.upper())
        img_bytes = img_bytes.getvalue()

        # Créer l'instance de CustomImage   
        wagtail_image = CustomImage(
            file=ContentFile(img_bytes, name=f"{document_type}_{document_collection.name}_{image_index}.jpeg"),
            title=f"{image_title} {image_index}",
            collection=document_collection
        )
        wagtail_image.save()
        wagtail_image.tags.add(*image_tags)
        return wagtail_image.id
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement de l'image {image_index}: {e}")
        return None

# Transformation du chart en image
def chart_to_img(document, image_title, image_tags, document_collection):
    print(colored("Conversion du chart en image", "green"))
    print(document)
    print(image_title)
    print(image_tags)
    print(document_collection)
    # try:
    #     # Convertir le chart en image
    #     img_bytes = BytesIO()
    #     document.save(img_bytes, format="PNG")
    #     img_bytes = img_bytes.getvalue()

    #     # Créer l'instance de CustomImage   
    #     wagtail_image = CustomImage(
    #         file=ContentFile(img_bytes, name=f"{document_collection.name}.png"),
    #         title=f"{image_title}",
    #         collection=document_collection
    #     )
    #     wagtail_image.save()
    #     wagtail_image.tags.add(*image_tags)
    #     return wagtail_image.id
    # except Exception as e:
    #     logger.error(f"Erreur lors de la transformation du chart en image: {e}")
    #     return None