import requests
from wagtail.admin import messages
from django.conf import settings
import os

from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from weasyprint import HTML, CSS
from django.http import HttpResponse

def generate_pdf(request, template_name, context, css_filenames, pdf_filename='convocation.pdf'):
    
    # Préparation du contenu HTML
    html_string = render_to_string(template_name, context)
    
    # Préparation des feuilles de style CSS
    stylesheets = []
    for css_filename in css_filenames:
        css_path = finders.find(css_filename)
        if css_path:
            stylesheets.append(CSS(filename=css_path))
            
    # Création de l'objet HTML avec WeasyPrint et ajout des CSS
    html = HTML(string=html_string)
    pdf = html.write_pdf(stylesheets=stylesheets)
    
    # Sauvegarde du PDF dans MEDIA_ROOT/documents
    media_path = os.path.join(settings.MEDIA_ROOT, 'documents', pdf_filename)
    with open(media_path, 'wb') as f:
        f.write(pdf)
    
    return media_path

def getPdfFromUrl(request, url, filename='convocation'):
    print('url', url)
    response = requests.get(url)
    if response.status_code == 200:
        media = settings.MEDIA_ROOT
        filepath = os.path.join(media, 'documents', f'{filename}.pdf')
        with open(filepath, 'wb') as f:
            f.write(response.content)
        messages.success(request, "Le fichier PDF a été téléchargé avec succès.")
        return filepath
    else:
        messages.error(request, "Impossible de télécharger le fichier PDF.")