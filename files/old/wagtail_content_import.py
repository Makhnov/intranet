
# # Import de fichiers textes 
# from wagtail_content_import.models import ContentImportMixin
# from wagtail_content_import.mappers.streamfield import StreamFieldMapper
# from wagtail_content_import.mappers.converters import BaseConverter, ImageConverter, RichTextConverter
# from wagtail.rich_text import RichText
# from wagtail_content_import.mappers.converters import (
#     ImageConverter, 
#     RichTextConverter, 
#     TableConverter, 
#     TextConverter,
# )

# # DOCX Mapper
# class DocxMapper(StreamFieldMapper):
#     html = RichTextConverter('docx_paragraphs')
#     image = ImageConverter('docx_images')
#     heading = TextConverter('docx_heading')
#     table = TableConverter('docx_tables')
    
# # DOCX Streamfield
# class DOCXStreamBlock(blocks.StreamBlock):
#     docx_heading = CharBlock()
#     docx_paragraphs = RichTextBlock()
#     docx_images = ImageChooserBlock()
#     docx_tables = TableBlock()

# # Import de DOCX (intégrée dans CompteRenduPage)
# class CustomDOCXBlock(ContentImportMixin, blocks.StructBlock):
#     mapper_class = DocxMapper
    
#     body = StreamField(DOCXStreamBlock, blank=True, null=True)   
#     docx_import = blocks.BooleanBlock(
#         required=False,
#         default=False,
#         label=_("Save and import"),
#         help_text=_("Use cautiously. It will override all existing content in this section."),
#     )

# # Import de DOCX
# class CustomDOCXPage(Page, ContentImportMixin):
#     mapper_class = DocxMapper
#     parent_page_types = ['home.HomePage']
#     subpage_types = []
    
#     body = StreamField(DOCXStreamBlock, blank=True, null=True)   
#     docx_import = models.BooleanField(
#         default=False,
#         verbose_name=_("Save and import"),
#         help_text=_("Use cautiously. It will override all existing content in this section."),
#     )    
#     # content
#     content_panels = Page.content_panels + [
#         FieldPanel("body"),
#         FieldPanel("docx_import"),
#     ]


# class HeadingBlockConverter(BaseConverter):
#     def __call__(self, element, **kwargs):
#         print(colored("ELEMENT SUCCESSFULLY MAPPED (HEADING)", "cyan", "on_white"))
#         return (self.block_name, {'heading_text': element['value'], 'size': 'h2'})

# class ParagraphBlockConverter(RichTextConverter):
#     def __call__(self, element, **kwargs):
#         if element.get('type') == 'html':
#             # Utilisez la méthode héritée pour convertir le HTML en format interne puis en RichText
#             cleaned_html = self.contentstate_converter.to_database_format(
#                 self.contentstate_converter.from_database_format(element["value"])
#             )

#             # Optionnel : convertir les liens externes si nécessaire
#             if getattr(settings, "WAGTAILCONTENTIMPORT_CONVERT_EXTERNAL_LINKS", True):
#                 cleaned_html = self.convert_external_links(cleaned_html)

#             print(colored("ELEMENT SUCCESSFULLY MAPPED (PARAGRAPH)", "magenta", "on_white"))
#             # Créez un objet RichText avec le HTML nettoyé
#             rich_text_value = RichText(cleaned_html)

#             # Renvoyez le bloc avec le contenu sous forme d'objet RichText
#             return (self.block_name, {'paragraph_text': rich_text_value, 'width': 'full'})

# class ImageBlockConverter(BaseConverter):
#     def __call__(self, element, user, **kwargs):
#         # Utilisez ImageConverter pour traiter l'image
#         image_url = element['value']
#         image_name, image_content = ImageConverter.fetch_image(image_url)
#         # Assurez-vous que l'utilisateur est bien passé en argument
#         image = ImageConverter.import_as_image_model(image_name, image_content, owner=user)
#         # Retournez le tuple attendu par StreamField avec le bloc 'image' configuré
#         return (self.block_name, {'image': image})


# class TableBlockConverter(BaseConverter):
#     def __call__(self, element, **kwargs):
#         # Extraction directe et simple de la valeur de la table
#         # Pour un traitement plus complexe, adaptez cette logique à votre structure de données spécifique
#         return (self.block_name, {'value': element['value']})


# # Heading Block
# class HeadingBlock(blocks.StructBlock):
#     heading_text = CharBlock(classname="title", required=True)
#     size = blocks.ChoiceBlock(choices=[
#         ('', 'Select a header size'),
#         ('h2', 'H2'),
#         ('h3', 'H3'),
#         ('h4', 'H4')
#     ], blank=True, required=False)
    
#     class Meta:
#         icon = "title"
#         template = "blocks/heading_block.html"

# # Paragraph Block
# class ParagraphBlock(blocks.StructBlock):
#     paragraph_text = blocks.RichTextBlock(required=True)
#     width = blocks.ChoiceBlock(choices=[
#         ('', 'Select a width'),
#         ('full', 'Full width'),
#         ('half', 'Half width'),
#         ('third', 'Third width'),
#         ('quarter', 'Quarter width'),
#     ], blank=True, required=False)
#     class Meta:
#         icon = "pilcrow"
#         template = "blocks/paragraph_block.html"
        
# # Image Block
# class ImageBlock(blocks.StructBlock):
#     show_full_image = blocks.BooleanBlock(required=False)
#     image = ImageChooserBlock()

#     class Meta:
#         icon = "image / picture"
#         admin_text = mark_safe("<b>Image Block</b>")
#         label = "Image Block"
#         template = "blocks/image_block.html"

# # Mapper
# class DocxMapper(StreamFieldMapper):
#     heading = HeadingBlockConverter('heading')
#     paragraph = ParagraphBlockConverter('paragraph')
#     image = ImageBlockConverter('image')
#     table = TableBlockConverter('table')
    
#     def map(self, elements, user=None, **kwargs):
#         print(colored(f"Elements : {elements}", "yellow", "on_white"))
#         mapped_elements = []
#         paragraph_buffer = []  # Pour stocker temporairement les paragraphes consécutifs

#         print(colored(f"START MAPPING", "green", "on_white"))

#         for element in elements:
            
#             # print(f"Mapping {element.get('type')} element: [[[{element.get('value')}]]]")  # Débogage
#             if element.get('type') == 'heading':    
#                 # Avant de mapper le titre, vérifiez si nous avons des paragraphes en attente dans le buffer
#                 if paragraph_buffer:
#                     # Fusionnez tous les paragraphes dans le buffer et ajoutez-les à mapped_elements
#                     merged_paragraph = self.merge_paragraphs(paragraph_buffer)
#                     mapped_elements.append(self.paragraph(merged_paragraph, **kwargs))
#                     paragraph_buffer = []  # Réinitialisez le buffer pour les futurs paragraphes
#                 mapped_elements.append(self.heading(element, **kwargs))
                
#             elif element.get('type') == 'image':
#                 # Vérifiez d'abord si nous avons des paragraphes en buffer
#                 if paragraph_buffer:
#                     merged_paragraph = self.merge_paragraphs(paragraph_buffer)
#                     if not self.is_void({'value': merged_paragraph}):
#                         mapped_elements.append(self.paragraph({'value': merged_paragraph}, **kwargs))
#                     paragraph_buffer = []
#                 # Ensuite, traitez l'image
#                 mapped_elements.append(self.image(element, **kwargs))

#             elif element.get('type') == 'table':
#                 # Même logique que pour les images
#                 if paragraph_buffer:
#                     merged_paragraph = self.merge_paragraphs(paragraph_buffer)
#                     if not self.is_void({'value': merged_paragraph}):
#                         mapped_elements.append(self.paragraph({'value': merged_paragraph}, **kwargs))
#                     paragraph_buffer = []
#                 mapped_elements.append(self.table(element, **kwargs))
                
#             elif element.get('type') == 'html':
#                 # Accumulez les paragraphes dans le buffer au lieu de les ajouter directement
#                 paragraph_buffer.append(element)
#         if paragraph_buffer:
#             merged_paragraph = self.merge_paragraphs(paragraph_buffer)
#             mapped_elements.append(self.paragraph(merged_paragraph, **kwargs))
            
#         print(colored(f"END MAPPING", "green", "on_white"))
#         return mapped_elements
    
#     def merge_paragraphs(self, paragraph_buffer):
#         merged_content = "".join([p['value'] for p in paragraph_buffer])
#         return {'type': 'html', 'value': merged_content}
        
# # Import de DOCX
# class CustomDOCXPage(Page, ContentImportMixin):
#     mapper_class = DocxMapper
#     parent_page_types = ['home.HomePage']
#     subpage_types = []

#     body = StreamField(
#         [
#             ("heading", HeadingBlock(icon="title")),
#             ("paragraph", ParagraphBlock(icon="pilcrow")),
#             ("image", ImageBlock(icon="image")),
#             ("table", TableBlock(icon="table")),
#         ],
#         use_json_field=True,
#         blank=True,
#         null=True,
#         verbose_name=_("Agenda"),
#         help_text=_("This is the main content of the page."),
#     )

#     docx_import = models.BooleanField(
#         default=False,
#         verbose_name=_("Save and import"),
#         help_text=_("Use cautiously. It will override all existing content in this section."),
#     )

#     content_panels = Page.content_panels + [
#         FieldPanel("body"),
#         FieldPanel("docx_import"),
#     ]
