
from wagtail.models import Orderable
from wagtail.documents.models import Document
from wagtail.fields import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Site

# Traductions
from django.utils.translation import gettext_lazy as _

# Icones
from dashboard.models import IntranetIcons
from utils.variables import FILE_EXTENSIONS

# Carrousel d'image (Galerie)
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
    
####################
##  UTILISATEURS  ##
#################### 

class CiviliteListe(models.TextChoices):
    H = 'Monsieur', _("Monsieur")
    F = 'Madame', _("Madame")
    N = 'Monsieur/Madame', _("Neutre")
                
class CommunesListe(models.TextChoices):
    ARBAS = "31011", "Arbas"
    ARBON = "31012", "Arbon"
    ARGUENOS = "31014", "Arguenos"
    ARNAUD_GUILHEM = "31018", "Arnaud-Guilhem"
    ASPET = "31020", "Aspet"
    AUSSEING = "31030", "Ausseing"
    AUZAS = "31034", "Auzas"
    BEAUCHALOT = "31050", "Beauchalot"
    BELBEZE_EN_COMMINGES = "31059", "Belbèze-en-Comminges"
    CABANAC_CAZAUX = "31095", "Cabanac-Cazaux"
    CASSAGNE = "31110", "Cassagne"
    CASTAGNEDE = "31112", "Castagnède"
    CASTELBIAGUE = "31114", "Castelbiague"
    CASTILLON_DE_SAINT_MARTORY = "31124", "Castillon-de-Saint-Martory"
    CAZAUNOUS = "31131", "Cazaunous"
    CHEIN_DESSUS = "31140", "Chein-Dessus"
    COURET = "31155", "Couret"
    ENCAUSSE_LES_THERMES = "31167", "Encausse-les-Thermes"
    ESCOULIS = "31591", "Escoulis"
    ESTADENS = "31174", "Estadens"
    FIGAROL = "31183", "Figarol"
    FOUGARON = "31191", "Fougaron"
    FRANCAZAL = "31195", "Francazal"
    LE_FRECHET = "31198", "Le Fréchet"
    GANTIES = "31208", "Ganties"
    HERRAN = "31236", "Herran"
    HIS = "31237", "His"
    IZAUT_DE_LHOTEL = "31241", "Izaut-de-l'Hôtel"
    JUZET_DIZAUT = "31245", "Juzet-d'Izaut"
    LAFFITE_TOUPIERE = "31260", "Laffite-Toupière"
    LESTELLE_DE_SAINT_MARTORY = "31296", "Lestelle-de-Saint-Martory"
    MANCIOUX = "31314", "Mancioux"
    MANE = "31315", "Mane"
    MARSOULAS = "31321", "Marsoulas"
    MAZERES_SUR_SALAT = "31336", "Mazères-sur-Salat"
    MILHAS = "31342", "Milhas"
    MONCAUP = "31348", "Moncaup"
    MONTASTRUC_DE_SALIES = "31357", "Montastruc-de-Salies"
    MONTESPAN = "31372", "Montespan"
    MONTGAILLARD_DE_SALIES = "31376", "Montgaillard-de-Salies"
    MONTSAUNES = "31391", "Montsaunès"
    PORTET_DASPET = "31431", "Portet-d'Aspet"
    PROUPIARY = "31440", "Proupiary"
    RAZECUEILLE = "31447", "Razecueillé"
    ROQUEFORT_SUR_GARONNE = "31457", "Roquefort-sur-Garonne"
    ROUEDE = "31461", "Rouède"
    SAINT_MARTORY = "31503", "Saint-Martory"
    SAINT_MEDARD = "31504", "Saint-Médard"
    SALEICH = "31521", "Saleich"
    SALIES_DU_SALAT = "31523", "Salies-du-Salat"
    SENGOUAGNET = "31544", "Sengouagnet"
    SEPX = "31545", "Sepx"
    SOUEICH = "31550", "Soueich"
    TOUILLE = "31554", "Touille"
    URAU = "31562", "Urau"

class FonctionsConseilListe(models.TextChoices):
    PRESIDENT = '1', "Président"
    VICEPRESIDENT = '2', "Vice-président"
    MEMBRE = '3', "Conseiller communautaire"
    SUPPLEANT = '4', "Délégué suppléant"

class FonctionsBureauListe(models.TextChoices):
    PRESIDENT = '1', "Président"
    VICEPRESIDENT = '2', "Vice-président"

class FonctionsConferenceListe(models.TextChoices):
    PRESIDENT = '1', "Président"
    VICEPRESIDENT = '2', "Vice-président"
    MEMBRE = '3', "Maire"
    
class FonctionsCommissionListe(models.TextChoices):
    PRESIDENT = '1', "Président"
    CHARGE = '2', "Chargé de commission"
    MEMBRE = '3', "Membre"

class FonctionsMairieListe(models.TextChoices):
    MAIRE = '1', "Maire"
    ADJOINT = '2', "Adjoint"
    CONSEILLER = '3', "Conseiller municipal"