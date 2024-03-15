from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from wagtail.search import index
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db import models
from wagtail.api import APIField

from utils.widgets import (
    CiviliteListe, 
    CommunesListe, 
    FonctionsMairieListe, 
    FonctionsConseilListe, 
    FonctionsBureauListe, 
    FonctionsConferenceListe,
    )

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
    commissions = models.ManyToManyField(
        'administration.CommissionPage',
        verbose_name=_("commissions"),
        blank=True,
    )
    functions_commissions = models.JSONField(
        default=list, 
        verbose_name=_("Functions in Commissions"),
        blank=True,
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
        APIField('commissions'),
        APIField('functions_commissions'),
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
        index.RelatedFields('commissions', [
            index.SearchField('title'),
        ]),
        index.SearchField('functions_commissions'),
        index.SearchField('function_bureau'),
        index.SearchField('function_conference'),
    ]
        
    class Meta:
        ordering = ["last_name"]
        
    def __str__(self):
        return f"{self.last_name.upper()} {self.first_name}"
