from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator
from wagtail.search import index
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db import models
from wagtail.api import APIField


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
             
class User(AbstractUser):
    # Ajout de la civilité pour les champs obligatoires
    civility = models.CharField(
        _("civility"),
        max_length=15,
        choices=CiviliteListe.choices,
        default=CiviliteListe.N,
    )
    # Ajout des champs supplémentaires (utilisateur)
    date_of_birth = models.DateField(
        verbose_name=_("Date of birth"), blank=True, null=True
    )
    address1 = models.CharField(
        verbose_name=_("Address line 1"), max_length=1024, blank=True, null=True
    )
    address2 = models.CharField(
        verbose_name=_("Address line 2"), max_length=1024, blank=True, null=True
    )
    zip_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=12, blank=True, null=True
    )
    city = models.CharField(
        verbose_name=_("City"), max_length=1024, blank=True, null=True
    )
    phone_regex = RegexValidator(
        regex=r"^\+(?:[0-9]●?){6,14}[0-9]$",
        message=_(
            "Enter a valid international mobile phone number starting with +(country code)"
        ),
    )
    mobile_phone = models.CharField(
        validators=[phone_regex],
        help_text=_("With country code and no spaces"),
        verbose_name=_("Mobile phone"),
        max_length=17,
        blank=True,
        null=True,
    )    
    # Ajout des champs spécifiques aux élus
    municipality = models.TextField(
        blank=True, 
        null=True,
        choices=CommunesListe.choices,
        # default=CommunesListe.NULL,
        verbose_name=_("municipality"),
    )
    function_municipality = models.TextField(
        blank=True, 
        null=True,
        choices=FonctionsMairieListe.choices,
        # default=FonctionsMairieListe.NULL,
        verbose_name=_("municipal council function"),
    )
    function_council = models.TextField(
        blank=True, 
        null=True,
        choices=FonctionsConseilListe.choices,
        # default=FonctionsConseilListe.NULL,
        verbose_name=_("communautary council function"),
    )
    commission = models.ForeignKey(
        'administration.CommissionPage', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        verbose_name=_("commission"),
    )
    function_commission = models.TextField(
        blank=True, 
        null=True,
        choices=FonctionsCommissionListe.choices,
        # default=FonctionsCommissionListe.NULL,
        verbose_name=_("commission function"),
    )
    function_bureau = models.TextField(
        blank=True, 
        null=True,
        choices=FonctionsBureauListe.choices,
        # default=FonctionsBureauListe.NULL,
        verbose_name=_("bureau function"),
    )
    function_conference = models.TextField(
        blank=True, 
        null=True,
        choices=FonctionsConferenceListe.choices,
        # default=FonctionsConferenceListe.NULL,
        verbose_name=_("mayor conference function"),
    )
    
    api_fields = [
        APIField('id'),
        APIField('detail_url'),
        APIField('type'),
        APIField('first_name'),
        APIField('last_name'),
        APIField('email'),
        APIField('groups'),
        APIField('user_permissions'),
        APIField('is_staff'),
        APIField('is_active'),
        APIField('date_joined'),
        APIField('last_login'),
        APIField('username'),
        APIField('civility'),
        APIField('date_of_birth'),
        APIField('address1'),
        APIField('address2'),
        APIField('zip_code'),
        APIField('city'),
        APIField('mobile_phone'),
        APIField('municipality'),
        APIField('function_municipality'),
        APIField('function_council'),
        APIField('commission'),
        APIField('function_commission'),
        APIField('function_bureau'),
        APIField('function_conference'),
    ]
    
    search_fields = [
        index.SearchField('civility'),
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('email'),
        index.FilterField('date_of_birth'),
        index.SearchField('address1'),
        index.SearchField('address2'),
        index.SearchField('zip_code'),
        index.SearchField('city'),
        index.SearchField('mobile_phone'),
        index.SearchField('municipality'),
        index.SearchField('function_municipality'),
        index.SearchField('function_council'),
        index.RelatedFields('commission', [
            index.SearchField('title'),
        ]),
        index.SearchField('function_commission'),
        index.SearchField('function_bureau'),
        index.SearchField('function_conference'),
    ]
        
    class Meta:
        ordering = ["last_name"]
        
    def __str__(self):
        return f"{self.last_name.upper()} {self.first_name}"
