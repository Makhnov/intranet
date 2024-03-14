from django import forms
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from wagtail.users.forms import UserEditForm, UserCreationForm
from .models import (
    User, 
    CiviliteListe,
    CommunesListe, 
    FonctionsMairieListe, 
    FonctionsConseilListe,   
    FonctionsCommissionListe,
    FonctionsBureauListe, 
    FonctionsConferenceListe,
)
from django.contrib.auth import get_user_model

def get_commission_queryset():
    CommissionPage = apps.get_model('administration', 'CommissionPage')
    return CommissionPage.objects.all()

class BaseUserForm:
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
    civility = forms.ChoiceField(
        choices=CiviliteListe.choices,
        label=_("Civility"),
        required=True,
    )
    municipality = forms.ChoiceField(
        choices=CommunesListe.choices,
        label=_("municipality"),
        required=False,
    )
    function_municipality = forms.ChoiceField(
        choices=FonctionsMairieListe.choices,
        label=_("municipal council function"),
        required=False,
    )
    function_council = forms.ChoiceField(
        choices=FonctionsConseilListe.choices,
        label=_("communautary council function"),
        required=False,
    )
    commissions = forms.ModelMultipleChoiceField(
        queryset=get_commission_queryset(),
        widget=forms.CheckboxSelectMultiple,
        label=_("commissions"),
        required=False,
    )
    functions_commissions = forms.MultipleChoiceField(
        choices=FonctionsCommissionListe.choices,
        widget=forms.CheckboxSelectMultiple,
        label=_("Functions in Commissions"),
        required=False,
    )
    function_bureau = forms.ChoiceField(
        choices=FonctionsBureauListe.choices,
        label=_("bureau function"),
        required=False,
    )
    function_conference = forms.ChoiceField(
        choices=FonctionsConferenceListe.choices,
        label=_("mayor conference function"),
        required=False,
    )

    def validate_elected_function(self):
        municipality = self.cleaned_data.get("municipality")
        verbose_municipality = self.instance.get_municipality_display() if self.instance and self.instance.pk else None
        # print("Commune :", verbose_municipality)
        commissions = self.cleaned_data.get("commissions")
        function_municipality = self.cleaned_data.get("function_municipality")
        function_council = self.cleaned_data.get("function_council")
        # print("function_council :", function_council)
        # function_commission = self.cleaned_data.get("function_commission")
        function_bureau = self.cleaned_data.get("function_bureau")
        function_conference = self.cleaned_data.get("function_conference")

        # Initialisation d'une variable queryset pour la validation
        users = User.objects.all()
        
        # Récupération de tous les utilisateurs associés à la même municipalité
        users_same_municipality = User.objects.filter(municipality=municipality).exclude(pk=self.instance.pk).exclude(function_council__isnull=True) 
        
        # print("Commune :", municipality)
        # Calcul des nombres de conseillers.
        council_members = users_same_municipality.filter(function_council__in=[1, 2, 3]).count()
        # print("Conseillers :", council_members)
        # Calcul des nombres de suppléants.
        substitutes = users_same_municipality.filter(function_council=4).count()
        # print("Substituts :", substitutes)
        
        # print(type(function_council))
        # print(type(substitutes))
        # print(type(council_members))

        # Vérifier si il y a plus d'un délégué communautaire ou déjà un suppléant
        # On ne peut plus rajouter de suppléant.
        if function_council == '4' and (council_members > 1 or substitutes > 0):
            # print("Erreur 1")
            self.add_error('function_council', _(f"They are already {council_members} council members and {substitutes} substitute(s) in {verbose_municipality}, therefore, you cannot add a substitute."))

        # Vérifier si il y a déjà un délégué suppléant et un conseiller communautaire
        # On ne peut rajouter ni de conseiller communautaire ni de suppléant.
        if function_council is not None and (substitutes == 1 and council_members == 1):
            # print("Erreur 2")
            self.add_error('function_council', _(f"They are already {substitutes} substitute and {council_members} council member(s) in {verbose_municipality}, you cannot add any more council members or substitutes."))

        # Si le formulaire est associé à une instance existante, excluez cette instance des validations
        if hasattr(self, 'instance') and self.instance.pk:
            users = users.exclude(pk=self.instance.pk)
            
        # Si pas de commune => pas de fonction au conseil municipal possible
        if not municipality and function_municipality:
            self.add_error('function_municipality', _("This user is not associated with a municipality. If you wish to add them to a municipal council, first choose the relevant municipality."))
            # Cet utilisateur n'est pas relié à une commune. Si vous souhaitez l'ajouter à un conseil municipal choisissez d'abord la commune concernée.

        # # Si pas de commission => pas de fonction en commission possible
        # if not commission and function_commission:
        #     self.add_error('function_commission', _("If there's no commission chosen, there can't be a commission role."))
        #     # Si pas de commission choisie, il ne peut pas y avoir de rôle au sein de la commission.

        # # Si pas de commune ni de fonction => pas de commission possible
        # if not function_municipality and not municipality and commission:
        #     self.add_error('commission', _("Only elected officials can serve. Choose both a municipality and a position within the municipal council before selecting a commission."))
        #     # Seuls les élus peuvent siéger. Choisissez une commune ET un poste au sein du conseil municipal avant de choisir une commission.

        # # Si pas de commune mais une fonction => pas de commission possible
        # elif not municipality and commission:
        #     self.add_error('commission', _("Only elected officials can serve. Choose a municipality before selecting a commission."))
        #     # Seuls les élus peuvent siéger. Choisissez une commune avant de choisir une commission.

        # # Si pas de fonction mais une commune => pas de commission possible
        # elif not function_municipality and commission:
        #     self.add_error('commission', _("Only elected officials can serve. Choose a function within the municipal council before selecting a commission."))
        #     # Seuls les élus peuvent siéger. Choisissez une fonction au conseil municipal avant de choisir une commission.

        # Si pas de commune ni de fonction => pas de fonction au conseil possible
        if not municipality and not function_municipality and function_council:
            self.add_error('function_council', _("A municipality and a municipal council role must be selected before choosing a community council role."))
            # Une commune et un rôle au conseil municipal doivent être sélectionnés avant de choisir un rôle au conseil communautaire.

        # Si pas de commune mais une fonction => pas de fonction au conseil possible
        elif not municipality and function_council:
            self.add_error('function_council', _("A municipality must be selected before choosing a community council role."))
            # Une commune doit être sélectionnée avant de choisir un rôle au conseil communautaire.

        # Si pas de fonction mais une commune => pas de fonction au conseil possible
        elif not function_municipality and function_council:
            self.add_error('function_council', _("A municipal council role must be selected before choosing a community council role."))
            # Un rôle au conseil municipal doit être sélectionné avant de choisir un rôle au conseil communautaire.

        # Si pas VP (function_council) OU pas P (function_council) => pas de fonction au bureau possible
        if function_council not in [FonctionsConseilListe.VICEPRESIDENT, FonctionsConseilListe.PRESIDENT] and function_bureau:
            self.add_error('function_bureau', _("Only the Vice-President or President of the community council can have a bureau role."))
            # Seuls le Vice-Président ou le Président du conseil communautaire peuvent avoir un rôle au bureau.

        # Si pas maire (function_municipality) OU pas VP (function_council) OU pas P (function_council) => pas de fonction à la conférence des maires possible
        if function_municipality != FonctionsMairieListe.MAIRE and function_council not in [FonctionsConseilListe.VICEPRESIDENT, FonctionsConseilListe.PRESIDENT] and function_conference:
            self.add_error('function_conference', _("Only the Mayor, Vice-President, or President of the community council can have a role in the Mayors' conference."))
            # Seuls le Maire, le Vice-Président ou le Président du conseil communautaire peuvent avoir un rôle à la conférence des maires.

        # Check if function is president and there's already a president in the database
        if function_council == FonctionsConseilListe.PRESIDENT and users.filter(function_council=FonctionsConseilListe.PRESIDENT).exists():
            self.add_error('function_council', _("There can only be one President of the council."))

        # Vérifier si la fonction est maire et s'il y a déjà un maire pour cette commune dans la base de données
        if function_municipality == FonctionsMairieListe.MAIRE and users.filter(municipality=municipality, function_municipality=FonctionsMairieListe.MAIRE).exists():
            self.add_error('function_municipality', _("There can only be one Mayor for each municipality."))

        # # Vérifier si la fonction est Président de commission et s'il y a déjà un président pour cette commission dans la base de données
        # if function_commission == FonctionsCommissionListe.PRESIDENT and users.filter(commission=commission, function_commission=FonctionsCommissionListe.PRESIDENT).exists():
        #     self.add_error('function_commission', _("There can only be one President for each commission."))

        # # Vérifier si la fonction est Chargé de commission et s'il y a déjà un chargé pour cette commission dans la base de données
        # if function_commission == FonctionsCommissionListe.CHARGE and users.filter(commission=commission, function_commission=FonctionsCommissionListe.CHARGE).exists():
        #     self.add_error('function_commission', _("There can only be one person in charge for each commission."))

        # # Vérifier si le chargé de commission est obligatoirement un Vice Président du conseil
        # if function_commission == FonctionsCommissionListe.CHARGE and function_council != FonctionsConseilListe.VICEPRESIDENT:
        #     self.add_error('function_commission', _("The person in charge of the commission must be a Vice President of the council."))
     
     
    def clean(self):
        cleaned_data = super().clean()
        self.validate_elected_function()
        return cleaned_data


class CustomUserCreationForm(BaseUserForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = list(UserCreationForm.Meta.fields) + [
            "civility",
            "date_of_birth",
            "municipality",
            "function_municipality",
            "function_council",
            "commissions",
            "functions_commissions",
            "function_bureau",
            "function_conference"
        ]
        model = User

    def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
            self.fields['date_of_birth'].widget = forms.DateInput(attrs={"type": "date"})

class CustomUserEditForm(BaseUserForm, UserEditForm):
    class Meta(UserEditForm.Meta):
        fields = list(UserEditForm.Meta.fields) + [
            "civility",
            "date_of_birth",
            "municipality",
            "function_municipality",
            "function_council",
            "commissions",
            "functions_commissions",
            "function_bureau",
            "function_conference"
        ]
        model = User
        
    def __init__(self, *args, **kwargs):
            super(CustomUserEditForm, self).__init__(*args, **kwargs)
            self.fields['date_of_birth'].widget = forms.DateInput(attrs={"type": "date"})

class CustomSettingsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "civility",
            "address1",
            "address2",
            "zip_code",
            "city",
            "mobile_phone",
            "date_of_birth",
        )
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
