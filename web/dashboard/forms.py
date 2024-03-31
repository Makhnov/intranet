from django import forms
from django.forms.models import ModelChoiceIteratorValue
from django.template.loader import get_template
from wagtail.models import Page
from django.contrib.contenttypes.models import ContentType

from administration.models import ConvocationPage, CompteRenduPage, ConseilsIndexPage, BureauxIndexPage, CommissionPage, ConferencesIndexPage
from amicale.models import AmicalePage
    
class CustomModelChoiceField(forms.ModelChoiceField):
    # widget=CustomSelect()
    
    def label_from_instance(self, obj):
        return obj.date.strftime("%d-%b-%Y")

class EmailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        # Récupère les ContentType pour chaque type de page
        amicale_type = ContentType.objects.get_for_model(AmicalePage)
        compte_rendu_type = ContentType.objects.get_for_model(CompteRenduPage)
        convocation_type = ContentType.objects.get_for_model(ConvocationPage)
        
        # Construit un queryset qui sélectionne les pages de ces types spécifiques
        pages = Page.objects.live().filter(content_type__in=[amicale_type, compte_rendu_type, convocation_type]).specific()


       # Définition des champs du formulaire pour les pages spécifiques
        self.fields['specific_page'] = forms.ChoiceField(choices=[], widget=forms.RadioSelect, label="Sélectionnez une page spécifique", required=False)

        # Remplissez le champ 'specific_page' avec vos pages spécifiques
        self.fields['specific_page'].choices = [
            ('conseil', 'Conseil'),
            ('bureau', 'Bureau'),
            # Ajoutez d'autres pages ici
        ]
        # # Champs pour les destinataires
        # self.fields['recipients'] = forms.CharField(widget=forms.Textarea, help_text="Séparer les adresses e-mail par une virgule", required=False)

        conseils_index_page = ConseilsIndexPage.objects.first()
        bureaux_index_page = BureauxIndexPage.objects.first()        
        conferences_index_page = ConferencesIndexPage.objects.first()    
        # commissions_page = CommissionPage.objects.all()
        
        # Définition des champs du formulaire pour les pages générales
        self.fields['page'] = forms.ModelChoiceField(queryset=pages, label="Sélectionnez une page", required=False)   
        
        self.fields['convocation_conseils'] = CustomModelChoiceField(
            queryset=ConvocationPage.objects.live().descendant_of(conseils_index_page).order_by('-date'),
            label="Sélectionnez une convocation (Conseils)",
            required=False
        )
        self.fields['convocation_bureaux'] = CustomModelChoiceField(
            queryset=ConvocationPage.objects.live().descendant_of(bureaux_index_page).order_by('-date'),
            label="Sélectionnez une convocation (Bureaux)",
            required=False
        )
        self.fields['convocation_conferences'] = CustomModelChoiceField(
            queryset=ConvocationPage.objects.live().descendant_of(conferences_index_page).order_by('-date'),
            label="Sélectionnez une convocation (Conferences)",
            required=False
        )
        
        self.field_order = ['choice', 'specific_page', 'page', 'convocation_conseils', 'convocation_bureaux', 'convocation_conferences']
        
        # # On boucle sur les commissions        
        # for commission in commissions_page:
        #     self.fields[f'commission_{commission.id}'] = CustomModelChoiceField(
        #         queryset=ConvocationPage.objects.live().descendant_of(commission).order_by('-date'),
        #         label=f'{commission.title} (Commission)',
        #         required=False
        #     )
        

# class CustomSelect(forms.Select):
#     template_name = "widgets/blocks/select.html"
#     option_template_name = "widgets/blocks/select_option.html"

#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

#         # Vérifie si 'value' est une instance de ModelChoiceIteratorValue et extrait l'ID réel
#         if isinstance(value, ModelChoiceIteratorValue):
#             real_value = value.value
#         else:
#             real_value = value

#         if real_value:
#             try:                
#                 page_object = self.choices.queryset.get(pk=real_value)
#                 option['attrs']['data-year'] = page_object.date.year
#                 option['attrs']['data-mail'] = getattr(page_object, 'mail', 'mail@default.com')
#                 option['attrs']['data-url'] = f'{page_object.url}/pdf'
#             except self.choices.queryset.model.DoesNotExist:
#                 # Gérer l'exception si l'objet n'est pas trouvé
#                 pass

#         return option