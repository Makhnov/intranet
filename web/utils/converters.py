from termcolor import colored
from django.conf import settings

from wagtail.rich_text import RichText
from wagtail_content_import.mappers.converters import BaseConverter, ImageConverter, RichTextConverter

class ParagraphBlockConverter(RichTextConverter):
    def __call__(self, element, **kwargs):
        if element.get('type') == 'html':
            # Utilisez la méthode héritée pour convertir le HTML en format interne puis en RichText
            cleaned_html = self.contentstate_converter.to_database_format(
                self.contentstate_converter.from_database_format(element["value"])
            )

            # Optionnel : convertir les liens externes si nécessaire
            if getattr(settings, "WAGTAILCONTENTIMPORT_CONVERT_EXTERNAL_LINKS", True):
                cleaned_html = self.convert_external_links(cleaned_html)

            print(colored("ELEMENT SUCCESSFULLY MAPPED (PARAGRAPH)", "magenta", "on_white"))
            # Créez un objet RichText avec le HTML nettoyé
            rich_text_value = RichText(cleaned_html)

            # Renvoyez le bloc avec le contenu sous forme d'objet RichText
            return (self.block_name, {'paragraph_text': rich_text_value, 'width': 'full'})
        
class HeadingBlockConverter(BaseConverter):
    def __call__(self, element, **kwargs):
        print(colored("ELEMENT SUCCESSFULLY MAPPED (HEADING)", "cyan", "on_white"))
        return (self.block_name, {'heading_text': element['value'], 'size': 'h2'})
    
class ImageBlockConverter(BaseConverter):
    def __call__(self, element, user, **kwargs):
        # Utilisez ImageConverter pour traiter l'image
        image_url = element['value']
        image_name, image_content = ImageConverter.fetch_image(image_url)
        # Assurez-vous que l'utilisateur est bien passé en argument
        image = ImageConverter.import_as_image_model(image_name, image_content, owner=user)
        # Retournez le tuple attendu par StreamField avec le bloc 'image' configuré
        return (self.block_name, {'image': image})

class TableBlockConverter(BaseConverter):
    def __call__(self, element, **kwargs):
        # Extraction directe et simple de la valeur de la table
        # Pour un traitement plus complexe, adaptez cette logique à votre structure de données spécifique
        return (self.block_name, {'value': element['value']})