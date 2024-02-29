# custom_content_panels
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# Téléchargement automatique des fichiers pour InstantDownloadPage
import zipfile
import io
from django.http import HttpResponse
from .models import InstantDownloadPage



# Panneaux de création de pages personnalisées
def custom_content_panels(exclude_fields=None):
    if exclude_fields is None:
        exclude_fields = []
    return [
        panel
        for panel in Page.content_panels
        if not (isinstance(panel, FieldPanel) and panel.field_name in exclude_fields)
    ]


# Panneaux de promotion de pages personnalisées
def custom_promote_panels(exclude_fields=None):
    if exclude_fields is None:
        exclude_fields = []

    new_panels = []

    for panel in Page.promote_panels:
        if isinstance(panel, MultiFieldPanel):
            children = panel.children
            new_children = []

            for child in children:
                if isinstance(child, FieldPanel) and child.field_name in exclude_fields:
                    new_child = FieldPanel(child.field_name, read_only=True)
                else:
                    # Cloner l'objet enfant pour éviter de le modifier en place
                    new_child = type(child)(child.field_name)
                new_children.append(new_child)

            # Cloner le MultiFieldPanel pour éviter de le modifier en place
            new_panel = MultiFieldPanel(new_children, heading=panel.heading)
        else:
            # Si ce n'est pas un MultiFieldPanel, vous pouvez simplement ajouter l'objet panel
            # Mais assurez-vous de cloner l'objet pour éviter de le modifier en place
            new_panel = type(panel)(panel.field_name)

        new_panels.append(new_panel)

    return new_panels


# Téléchargement automatique des fichiers pour InstantDownloadPage
def download_document(request, page_id):
    page = InstantDownloadPage.objects.get(pk=page_id)
    documents = page.download_documents.all()

    if len(documents) == 1:
        document = documents[0].document
        response = HttpResponse(document.file.read(), content_type=document.file_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % document.filename
        return response
    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for doc in documents:
                zip_file.writestr(doc.title, doc.document.file.read())
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="documents.zip"'
        return response

 #
