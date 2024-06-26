import re
from django import forms
from django.forms import ModelChoiceField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList

from administration.models import ConvocationPage, ConseilsIndexPage, BureauxIndexPage, CommissionPage, ConferencesIndexPage
from amicale.models import AmicalePage
from home.models import RessourcesPage, PublicPage

class ConvocationChoiceField(ModelChoiceField):    
    def label_from_instance(self, obj):
        return obj.date.strftime("%d-%b-%Y")


#######################################
##  SECTION HAUTE (Champ caché: PDF) ##
#######################################  
class TopSection(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Champ caché pour stocker la sélection actuelle de la colonne de droite
        self.fields['pdf_page'] = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':"pdf-page"}), required=False)
        
        # Champ caché pour stocker les infos sur le document PDF
        self.fields['pdf_file'] = forms.JSONField(widget=forms.HiddenInput(attrs={'id':"pdf-file"}), required=False)

#######################################
##  SECTION GAUCHE (Amicale, autres) ##
#######################################  
class LeftSection(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        

        # Définition des champs du formulaire pour les pages spécifiques
        self.fields['left_pages'] = forms.ChoiceField(
            choices=[], 
            widget=forms.RadioSelect(attrs={'data-name': "left_pages"}), 
            label="Sélectionnez un type de page", 
            help_text="Y compris pour générer un PDF (bouton en haut à droite)", 
            required=False
        )
        self.fields['left_pages'].choices = [
            ('amicale', "Pages de l'amicale"),
            ('ressources', "Pages ressources (privées)"),
            ('public', "Pages publiques"),
        ]        
        # On récupère les pages d'index ressources et publiques
        resources_index_page = RessourcesPage.objects.first()
        public_index_page = PublicPage.objects.first()   
             
        # Queryset Amicale, Ressources et Publiques
        amicale = AmicalePage.objects.live().specific().order_by('-date')
        ressources = resources_index_page.get_children().live().specific().order_by('title')
        public = public_index_page.get_children().live().specific().order_by('title')   
        
        # Choix de la page de l'amicale
        self.fields['amicale'] = ModelChoiceField(
            queryset=amicale,
            label="Sélectionnez une page de l'amicale",
            required=False
        )
        # Choix de la page ressources
        self.fields['ressources'] = ModelChoiceField(
            queryset=ressources,
            label="Sélectionnez une page privée",
            required=False
        )
        # Choix de la page publique
        self.fields['public'] = ModelChoiceField(
            queryset=public,
            label="Sélectionnez une page publique",
            required=False
        )        
        # Champs pour les destinataires
        self.fields['mail_to'] = forms.CharField(label="Destinataires", widget=forms.Textarea, help_text="Séparer les adresses e-mail par une virgule", required=False)
        
        # Télécharger ou non un document sur cette page (booléen)
        self.fields['left_attachments'] = forms.BooleanField(label="Attacher les pièces-jointes", required=False)


    def clean_mail_to(self):
        data = self.cleaned_data['mail_to']
        if not data:
            return []
        
        # Permettre les séparations par virgule ou point-virgule, avec ou sans espaces blancs
        separator_pattern = r'\s*[,;]\s*'
        emails = re.split(separator_pattern, data)

        # Vérifiez chaque adresse e-mail pour s'assurer qu'elle est valide
        for email in emails:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(f"L'adresse e-mail '{email}' n'est pas valide.")

        # Retournez les e-mails vérifiés comme une liste
        return emails

#######################################
##   SECTION DROITE (Convocations)   ##
####################################### 
class RightSection(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définition des champs du formulaire pour les pages générales
        self.fields['right_pages'] = forms.ChoiceField(
            choices=[],
            widget=forms.RadioSelect(attrs={'data-name': "right_pages"}),
            label="Sélectionnez une type de page",
            help_text="Y compris pour générer un PDF (bouton en haut à droite)",
            required=False
        )

        self.fields['right_pages'].choices = [
            ('conseils', "Page des conseils"),
            ('bureaux', "Page des bureaux"),
            ('conferences', "Page des conférences"),
            ('commissions', "Page des commissions"),
        ]        
        # On prépare le champ de la séléction des commissions (sans choice pour commencer)
        self.fields['commissions'] = forms.ChoiceField(
            choices=[], 
            widget=forms.RadioSelect(attrs={'data-name': "commissions"}), 
            label="Sélectionnez une commission ou un groupe de travail", 
            required=False
        )
        commissions_choices = []
        
        # On récupère les index des pages de conseils, bureaux et conférences (ainsi que tous les index des commissions)
        conseils_index_page = ConseilsIndexPage.objects.first()
        bureaux_index_page = BureauxIndexPage.objects.first()        
        conferences_index_page = ConferencesIndexPage.objects.first()    
        commissions_page = CommissionPage.objects.all()
        
        # Choix d'une page de conseil
        self.fields['conseils'] = ConvocationChoiceField(
            queryset=ConvocationPage.objects.live().descendant_of(conseils_index_page).order_by('-date'),
            label="Convocation(s) Conseil",
            required=False
        )        
        # Choix d'une page de bureau
        self.fields['bureaux'] = ConvocationChoiceField(
            queryset=ConvocationPage.objects.live().descendant_of(bureaux_index_page).order_by('-date'),
            label="Convocation(s) Bureau",
            required=False
        )        
        # Choix d'une page de conférence
        self.fields['conferences'] = ConvocationChoiceField(
            queryset=ConvocationPage.objects.live().descendant_of(conferences_index_page).order_by('-date'),
            label="Convocation(s) Conférence",
            required=False
        )
        # Ordre des champs
        self.field_order = ['right_pages', 'commissions', 'convocation_conseils', 'convocation_bureaux', 'convocation_conferences']
        commissions_order = []
        
        # On boucle sur les commissions        
        for commission in commissions_page:            
            # On ajoute chaque commission au field du choix de commissions
            commissions_choices.append((f'commission_{commission.id}', commission.title))
               
            # On ajoute ce champ à l'ordre des champs
            commissions_order.append(f'commission_{commission.id}')
            
            # Ensuite on créé un champ pour chaque commission
            self.fields[f'commission_{commission.id}'] = ConvocationChoiceField(
                queryset=ConvocationPage.objects.live().descendant_of(commission).order_by('-date'),
                label=f'Convocation(s) {commission.title}',
                required=False
            )
            
        # Mise à jour des choices du champ 'commissions' avec la nouvelle liste
        self.fields['commissions'].choices = commissions_choices
        
        # Mise à jour de l'ordre des champs    
        self.field_order.extend(commissions_order)
        
        # Télécharger ou non un document sur cette page (booléen)
        self.fields['right_attachments'] = forms.BooleanField(label="Attacher les pièces-jointes", required=False)
        self.field_order.append('right_attachments')
        
#######################################
##       FORMULAIRE  PRINCIPAL       ##
####################################### 
class EmailForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if request and request.method == 'POST':
            self.top_section = TopSection(request.POST, request.FILES, prefix='top')
            self.left_section = LeftSection(request.POST, prefix='left')
            self.right_section = RightSection(request.POST, prefix='right')
        else:
            self.top_section = TopSection(prefix='top')
            self.left_section = LeftSection(prefix='left')
            self.right_section = RightSection(prefix='right')