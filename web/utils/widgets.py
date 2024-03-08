
from wagtail.models import Orderable
from wagtail.documents.models import Document

from wagtail.fields import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# Traductions
from django.utils.translation import gettext_lazy as _

# Carrousel d'image (HomePage)
class GalleryImage(Orderable):
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
    
    class Meta:
        abstract = True

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
