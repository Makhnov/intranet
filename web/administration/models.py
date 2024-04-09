from termcolor import colored
import uuid
from datetime import datetime
from django.utils.timezone import now
from collections import defaultdict

from django.utils.timezone import make_aware
from django.db import models
from django import forms

from wagtail.models import Page

# Fields
from wagtail.fields import RichTextField, StreamField
from wagtail.search.backends import get_search_backend
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    PageChooserPanel,
    MultiFieldPanel,
)

# Blocks
from wagtail.blocks import (
    CharBlock,
    RichTextBlock,
    ListBlock,
    BlockQuoteBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

# Parentalkey 
from modelcluster.fields import ParentalKey

# Page de menu
from utils.menu_pages import MenuPage, menu_page_save, TYPE_CHOICES
from utils.variables import TABLE_OPTIONS, POSITIONS_TRANSLATIONS

# Custom panels
from home.views import custom_content_panels, custom_promote_panels

# Tables
from wagtail.contrib.table_block.blocks import TableBlock

# Blocks, Medias, PJ, etc.
from utils.widgets import PiecesJointes as PJBlock
from utils.streamfield import (
    CustomMediaBlock as MediaBlock,
    CustomLinkBlock as LinkBlock,
    CustomEmbedBlock as EmbedBlock,
    CustomPDFBlock as PDFBlock,
    CustomDOCXBlock as DOCXBlock,
)

# Export PDF
from wagtail_pdf_view.mixins import PdfViewPageMixin

# API
from wagtail.api import APIField

# Traduction
from django.utils.translation import gettext_lazy as _

# Recherche
from wagtail.search import index

# Utilisateurs
from django.contrib.auth import get_user_model
User = get_user_model()
def get_active_users():
    return User.objects.filter(is_active=True)

####################
## PAGES DE MENUS ##
#################### 

# Accueil de la section administration du site
class AdministrationIndexPage(MenuPage):
    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "administration.ConseilsIndexPage",
        "administration.BureauxIndexPage",
        "administration.CommissionsIndexPage",
        "administration.ConferencesIndexPage",
    ]
    save = menu_page_save('administration')

# Index des conseils
class ConseilsIndexPage(MenuPage):
    parent_page_types = ["administration.AdministrationIndexPage"]
    subpage_types = ["administration.ConvocationPage", "administration.CompteRenduPage"]
    save = menu_page_save('conseils')
    
    label = models.SlugField(
        blank=True,
        verbose_name=_("Label"),
        help_text=_("Le texte qui apparaitra dans le titre des convocations et des comptes-rendus."),
        max_length=15,
        allow_unicode=False,
    )
    
    # Panneau de contenu
    content_panels = MenuPage.content_panels + [
        FieldPanel("label"),        
    ]
    
    def get_members(self):
        members = get_active_users().filter(function_council__isnull=False)
        members_sorted = {
            "Président": [],
            "Présidente": [],
            "Vice-présidents": [],
            "Délégués communautaires (titulaires)": [],
            "Délégués communautaires (suppléants)": [],
        }        
        for member in members:
            function = member.function_council
            if function == "1":
                if member.civility == "Madame":
                    members_sorted['Présidente'].append(member)
                else:
                    members_sorted['Président'].append(member)
            elif function == "2":
                members_sorted['Vice-présidents'].append(member)
            elif function == "3":
                members_sorted['Délégués communautaires (titulaires)'].append(member)
            elif function == "4":
                members_sorted['Délégués communautaires (suppléants)'].append(member)                                
        # print(colored("members_sorted", "green"), colored(members_sorted, "white", "on_green"))
        return members_sorted
    
    def get_context(self, request):
        context = super().get_context(request)
        context['children'] = cv_cr_filter(self, request)
        context['members'] = self.get_members()
        return context
        
    class Meta:
        verbose_name = "conseil"
        verbose_name_plural = "conseils"

# Index des bureaux
class BureauxIndexPage(MenuPage):
    parent_page_types = ["administration.AdministrationIndexPage"]
    subpage_types = ["administration.ConvocationPage", "administration.CompteRenduPage"]
    save = menu_page_save('bureaux')

    label = models.SlugField(
        blank=True,
        verbose_name=_("Label"),
        help_text=_("Le texte qui apparaitra dans le titre des convocations et des comptes-rendus."),
        max_length=15,
        allow_unicode=False,
    )
    
    # Panneau de contenu
    content_panels = MenuPage.content_panels + [
        FieldPanel("label"),        
    ]
    
    def get_members(self):
        members = get_active_users().filter(function_bureau__isnull=False)
        members_sorted = {
            "Président": [],
            "Présidente": [],
            "Vice-présidents": [],
        }
        for member in members:
            function = member.function_bureau
            if function == "1":
                if member.civility == "Madame":
                    members_sorted['Présidente'].append(member)
                else:
                    members_sorted['Président'].append(member)
            elif function == "2":
                members_sorted['Vice-présidents'].append(member)
        # print(colored("members_sorted", "green"), colored(members_sorted, "white", "on_green"))
        return members_sorted


    def get_context(self, request):
        context = super().get_context(request)
        context['children'] = cv_cr_filter(self, request)
        context['members'] = self.get_members()
        return context
    
    class Meta:
        verbose_name = "bureau"
        verbose_name_plural = "bureaux"

# Index des commissions
class ConferencesIndexPage(MenuPage):
    parent_page_types = ["administration.AdministrationIndexPage"]
    subpage_types = ["administration.ConvocationPage", "administration.CompteRenduPage"]
    save = menu_page_save('conferences')
    
    label = models.SlugField(
        blank=True,
        verbose_name=_("Label"),
        help_text=_("Le texte qui apparaitra dans le titre des convocations et des comptes-rendus."),
        max_length=15,
        allow_unicode=False,
    )

    # Panneau de contenu
    content_panels = MenuPage.content_panels + [
        FieldPanel("label"),        
    ]

    def get_members(self):
        members = get_active_users().filter(function_conference__isnull=False)
        members_sorted = {
            "Président": [],
            "Présidente": [],
            "Maires": [],
            "Vice-présidents": [],
        }        
        for member in members:
            function = member.function_conference
            if function == "1":
                if member.civility == "Madame":
                    members_sorted['Présidente'].append(member)
                else:
                    members_sorted['Président'].append(member)
            elif member.function_municipality == "1":
                members_sorted['Maires'].append(member)
            elif function == "2":
                members_sorted['Vice-présidents'].append(member)                
        # print(colored("members_sorted", "green"), colored(members_sorted, "white", "on_green"))
        return members_sorted
        
    
    def get_context(self, request):
        context = super().get_context(request)
        context['children'] = cv_cr_filter(self, request)
        context['members'] = self.get_members()
        return context
    
    class Meta:
        verbose_name = "conférence"
        verbose_name_plural = "conférences"

# Index des commissions et groupes de travail
class CommissionsIndexPage(MenuPage):
    parent_page_types = ["administration.AdministrationIndexPage"]
    subpage_types = ["administration.CommissionPage"]
    save = menu_page_save('commissions')

    class Meta:
        verbose_name = "Commissions (Index)"

# Index d'une commission ou d'un groupe de travail
class CommissionPage(Page):
    parent_page_types = ["administration.CommissionsIndexPage"]
    subpage_types = ["administration.ConvocationPage", "administration.CompteRenduPage"]
    max_count = None
    show_in_menus_default = True
    
    logo = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo (SVG, png, jpg, etc.)"),
        help_text=_("𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦: Round or square (1/1). 𝐈𝐝𝐞𝐚𝐥 𝐟𝐨𝐫𝐦𝐚𝐭: Filled SVG. 𝐒𝐞𝐜𝐨𝐧𝐝𝐚𝐫𝐲 𝐟𝐨𝐫𝐦𝐚𝐭: PNG with transparent background."),
    )
    heading = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Heading"),
        help_text=_("Displayed in menus, the heading is the title of the page."),
    )
    tooltip = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Tooltip"),
        help_text=_("Used for accessibility (alt, title) and when user mouse over the icon."),
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='commission',
        blank=False,
        null=False,
        verbose_name=_("Type"),
        help_text=_("Choose if this is a commission or a working group."),
    )
    label = models.SlugField(
        blank=True,
        verbose_name=_("Label"),
        help_text=_("Le texte qui apparaitra dans le titre des convocations et des comptes-rendus."),
        max_length=15,
        allow_unicode=False,
    )

    # Panneau de contenu
    content_panels = Page.content_panels + [
        MultiFieldPanel([
                FieldPanel("logo"),
                FieldPanel("heading"),
                FieldPanel("tooltip"),
            ],
            heading=_("Menu display options (click to expand)"),
            help_text=_("Choose an icon and a tooltip to display on the index pages. Both optional, if none, CGS logo will be the icon and tooltip will refer as the page title"),
            classname="collapsible, collapsed",
        ),
        FieldPanel("type"),
        FieldPanel("label"),        
    ]
    
    def get_members(self):
        # Initialisation du dictionnaire pour trier les membres
        members_sorted = {
            "Chargé de commission": [],
            "Chargée de commission": [],            
            "Président": [],
            "Présidente": [],
            "Membres": [],
        }
                
        # Filtrer les utilisateurs liés à cette commission
        users = get_active_users().filter(commissions=self)
                
        for user in users:
            commission_ids = user.commissions.values_list('id', flat=True)
            # print(f'{user.get_full_name()} est membre des commissions {commission_ids}')

            # Trouver la fonction correspondante dans `functions_commissions` pour cette commission
            function_entry = next((entry for entry in user.functions_commissions if entry['commission'] == str(self.id)), None)
            
            if function_entry:
                # print("function_entry :", function_entry)
                function = function_entry['function']                
                # print("function :", function)
                
                # Identifier la fonction de l'utilisateur et ajouter à la catégorie correspondante
                if function == '1':
                    if user.civility == 'Madame':
                        members_sorted["Présidente"].append(user)
                    else:
                        members_sorted["Président"].append(user)
                elif function == '2':
                    if user.civility == 'Madame':
                        members_sorted["Chargée de commission"].append(user)
                    else:
                        members_sorted["Chargé de commission"].append(user)
                elif function == '3':
                    members_sorted["Membres"].append(user)
                        
        # print(colored("members_sorted", "green"), colored(members_sorted, "white", "on_green"))
        return members_sorted


    def get_context(self, request):
        context = super().get_context(request)
        commissions_index_page = Page.objects.get(slug="commissions")
        context['menu_type'] = self.slug
        context['child_type'] = self.slug
        context['children'] = cv_cr_filter(self, request)
        context['commissions_menu'] = commissions_index_page.get_children().live()
        context['members'] = self.get_members()
        return context
        
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "commission ou groupe de travail"
        verbose_name_plural = "commissions ou groupes de travail"

####################################
## CONVOCATIONS ET COMPTES-RENDUS ##
#################################### 

# Convocation aux instances
class ConvocationPage(PdfViewPageMixin, Page):
    parent_page_types = [
        "administration.ConseilsIndexPage",
        "administration.BureauxIndexPage",
        "administration.CommissionPage",
        "administration.ConferencesIndexPage",
    ]
    subpage_types = []
    show_in_menus_default = True
    template_name = "administration/conseils/convocation_page.html"
    admin_template_name = "administration/conseils/convocation_page.html"
    ROUTE_CONFIG = [
        ("html", r'^$'),
        ("pdf", r'^pdf/$'),
    ]
    
    date = models.DateTimeField(verbose_name="Date")
    old = models.BooleanField(verbose_name=_("Old"), default=False, blank=True, null=True)
    body = RichTextField(blank=True, verbose_name=_("Agenda"))

    content_panels = custom_content_panels(["title"]) + [
        FieldPanel("date", attrs={'data-id': "date"}),
        FieldPanel("body", attrs={'data-id': "body"}),
        InlinePanel(
            "convocation_documents",
            label=_("Document"),
            heading=_("Attachments"),
            classname="collapsible",
            attrs={'data-id': "attachments"},
        ),
    ]
    promote_panels = custom_promote_panels(["slug"])
        
    api_fields = [   
        APIField('old'),
        APIField('date'),
        APIField('body'),
        APIField('convocation_users'),
    ]
    
    search_fields = Page.search_fields + [ 
        index.SearchField('title'),
        index.FilterField('date'),
        index.SearchField('body'),
    ]
    
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = "Convocation"
        if not self.slug or self.slug == "convocation":
            unique_suffix = uuid.uuid4().hex[:6]  # Génère un suffixe unique
            self.slug = f"convocation-{unique_suffix}"
        super().save(*args, **kwargs)
    
    def get_parent_type(self):
        parent = self.get_parent()
        if parent:
            return parent.specific_class
        return None
    
    def convocation_page_view(request, page_id):
        page = ConvocationPage.objects.get(id=page_id)
        return page.serve_pdf(request)

    def get_convocation_users(self):
        return self.convocation_users.all()
    
    def get_context(self, request, **kwargs):
        context = super().get_context(request, **kwargs)
        context['is_pdf'] = 'pdf' in request.path
        context['old'] = self.old
        parent = self.get_parent().specific
        context['parent'] = parent

        if hasattr(parent, 'get_members'):
            members = parent.get_members()
            hosts = []
            for president in members.get('Président', []) + members.get('Présidente', []):
                hosts.append({
                    'civility': president.civility,
                    'function': 'Président' if president.civility == 'Monsieur' else 'Présidente',
                    'name': f"{president.first_name} {president.last_name}",  # Ajout du nom complet
                    'object': president,
                })
            if parent.__class__.__name__ == 'CommissionPage':
                for charge in members.get('Chargé de commission', []) + members.get('Chargée de commission', []):
                    hosts.append({
                        'civility': charge.civility,
                        'function': 'Chargé de commission' if charge.civility == 'Monsieur' else 'Chargée de commission',
                        'name': f"{charge.first_name} {charge.last_name}",  # Ajout du nom complet
                        'object': charge,
                    })
            context['hosts'] = hosts

        if hasattr(parent, 'get_children'):
            start = self.date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)            
            end = self.date
            
            # On récupère les convocations précédentes de la même année
            siblings = ConvocationPage.objects.live().descendant_of(parent).filter(date__range=(start, end)).order_by('date')
            position = siblings.count()
            
            # Traduction littérale (et genrée)
            position_m = POSITIONS_TRANSLATIONS['M'].get(position, "{}e".format(position))
            position_f = POSITIONS_TRANSLATIONS['F'].get(position, "{}e".format(position))

            # On ajoute les variables au contexte
            context['position_m'] = position_m
            context['position_f'] = position_f
            
            
        return context
    
    def get_template(self, request, *args, **kwargs):
        parent_page = self.get_parent().specific
        if isinstance(parent_page, CommissionPage):
            template_path = "administration/commissions/convocation_page.html"
        else:
            parent_page_slug = parent_page.slug
            template_path = f"administration/{parent_page_slug}/convocation_page.html"
        return template_path
    
    class Meta:
        verbose_name = "convocation"
        verbose_name_plural = "convocations"
    
# Compte-rendu des instances
class CompteRenduPage(PdfViewPageMixin, Page):
    parent_page_types = [
        "administration.ConseilsIndexPage",
        "administration.BureauxIndexPage",
        "administration.CommissionPage",
        "administration.ConferencesIndexPage",
    ]
    subpage_types = []
    show_in_menus_default = True
    template_name = "administration/conseils/compte_rendu_page.html"
    admin_template_name = "administration/conseils/compte_rendu_page.html"
    ROUTE_CONFIG = [
        ("html", r'^$'),
        ("pdf", r'^pdf/$'),
    ] 
    
    convocation = models.OneToOneField(
        "ConvocationPage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name=_("Convocation"),
        help_text=_("Sélectionnez la convocation associée."),
        unique=True,
    )
    secretary = models.ForeignKey(
        User,
        verbose_name=_("Secrétaire"),
        blank=True,
        null=True,
        related_name='secretary_cr',
        on_delete=models.SET_NULL,
    )
    substitute_users = models.ManyToManyField(
        User,
        verbose_name=_("Remplaçants"),
        blank=True,
        related_name='substitute_cr',
    )
    replaced_users = models.ManyToManyField(
        'administration.ConvocationUser',
        verbose_name=_("Excusés et remplacés"),
        blank=True,
        related_name='replaced_cr',
    )
    unreplaced_users = models.ManyToManyField(
        'administration.ConvocationUser',
        verbose_name=_("Excusés non remplacés"),
        blank=True,
        related_name='unreplaced_cr',
    )
    date = models.DateTimeField(verbose_name="Date", null=True, blank=True)
    quorum = models.BooleanField(
        default=True,
        verbose_name=_("Quorum"),
        help_text=_("Uncheck this box if the quorum isn't reached"),
    )    
    body = StreamField(
        [
            ("heading", CharBlock(classname="title", icon="title", label=_("Heading"))),
            ("paragraph", RichTextBlock(icon="pilcrow", label=_("Paragraph"))),
            ("media", MediaBlock(icon="media", label=_("Media"))),
            ("image", ImageChooserBlock(icon="image", label=_("Image"))),
            ("document", DocumentChooserBlock(icon="doc-full", label=_("Document"))),
            ("link", LinkBlock(icon="link", label=_("Link"))),
            ("embed", EmbedBlock(icon="media", label=_("Embed media"))),
            ("list", ListBlock(CharBlock(icon="list-ul", label=_("List Item")), icon="list-ul", label=_("List"))),
            ("quote", BlockQuoteBlock(icon="openquote", label=_("Quote"))),
            ("table", TableBlock(table_options=TABLE_OPTIONS, icon="table", label=_("Table"))),
            ("PDF", PDFBlock(icon="doc-full", label=_("PDF"))),
            ("DOCX", DOCXBlock(icon="doc-full", label=_("DOCX"))),
        ],
        use_json_field=True,
        blank=True,
        null=True,
        verbose_name=_("Main review"),
        help_text=_("This is the main content of the page."),
    )
    content_panels = custom_content_panels(["title"]) + [
        PageChooserPanel("convocation", "administration.ConvocationPage", attrs={'data-id': "convocation"}),
        MultiFieldPanel(
            [
                FieldPanel("secretary", widget=forms.Select, classname="instance_secretary col4", attrs={'data-id': "secretary"}),
                FieldPanel("date", read_only=True, classname="instance_date col4", attrs={'data-id': "date"}),
                FieldPanel("quorum", classname="instance_quorum col4", attrs={'data-id': "quorum"}),
            ],
            heading=_("Instance management"),
            classname="collapsible col12",
            attrs={'data-id': "settings"},
        ),
        MultiFieldPanel(
            [
                FieldPanel(
                    "replaced_users", 
                    widget=forms.CheckboxSelectMultiple,
                    classname="instance_replaced col6",
                    attrs={'data-id': "replaced"},
                ),
                FieldPanel(
                    "unreplaced_users", 
                    widget=forms.CheckboxSelectMultiple,
                    classname="instance_unreplaced col6",
                    attrs={'data-id': "unreplaced"},
                ),
            ],
            heading=_("Absence management"),
            classname="collapsible collapsed col12",
            attrs={'data-id': "absences"},
        ),
        FieldPanel(
            "body",
            attrs={'data-id': "body"},
        ),
        InlinePanel(
            "compte_rendu_documents",
            label=_("Document"),
            heading=_("Attachments"),
            classname="collapsible",
            attrs={'data-id': "attachments"},
        ),
    ]
    promote_panels = custom_promote_panels(["slug"])
            
    api_fields = [
        APIField('convocation'),
        APIField('secretary'),
        APIField('substitute_users'),
        APIField('replaced_users'),
        APIField('unreplaced_users'),   
        APIField('date'),
        APIField('quorum'),
        APIField('body'),
    ]
    
    search_fields = Page.search_fields + [ 
        index.SearchField('title'),
        index.SearchField('body'),
        index.SearchField('convocation'),                                                 
        index.FilterField('date'),
        index.RelatedFields('secretary', [
            index.SearchField('username'),
        ]),
    ]
    
    def save(self, *args, **kwargs):
        if not self.title:  # Si le titre n'est pas déjà défini
            self.title = "compte-rendu"
        if not self.slug:  # Si le slug n'est pas déjà défini
            self.slug = "compte-rendu"
        super().save(*args, **kwargs)

    def get_parent_type(self):
        parent = self.get_parent()
        if parent:
            return parent.specific_class
        return None

    def get_context(self, request, **kwargs):
        context = super().get_context(request, **kwargs)
        context['is_pdf'] = 'pdf' in request.path
        context['parent'] = self.get_parent().specific
        
        # On s'assure que la page a une convocation associée
        if self.convocation is not None:
            
            # On ajoute au contexte le statut 'old' de la convocation
            context['old'] = self.convocation.old            
            # print(colored("old", "green"), colored(context['old'], "white", "on_green"))
            
            convocation_users = ConvocationUser.objects.filter(
                convocation=self.convocation
            ).select_related('user', 'substitute', 'alternate').order_by('function_weight', 'user__municipality')

            # Initialisation des listes pour les différentes catégories
            titulars = []
            alternates = []
            replaced = []
            excused = []
            
            # Parcourir tous les utilisateurs de la convocation
            for cu in convocation_users:
                user_info = {
                    "identity": cu.user.get_full_name(),
                    "municipality": cu.user.get_municipality_display(),
                    "function_weight": cu.function_weight,
                    "function": cu.function,
                    "civility": cu.user.civility,
                }
                
                if cu.presence == PresenceStatus.PRESENT:
                    # 1/ Les Titulaires présents
                    titulars.append(user_info)
                    
                elif cu.alternate and cu.alternate == cu.substitute:
                    # 2/ Les suppléants présents
                    alternates.append({
                        "identity": cu.alternate.get_full_name(),
                        "municipality": cu.alternate.get_municipality_display(),
                    })
                    # Ajoute également le titulaire à la liste des absents excusés
                    excused.append(user_info)
                elif cu.presence == PresenceStatus.REPLACED and cu.alternate != cu.substitute:
                    # 3/ Les absents excusés ayant donné procuration
                    replaced.append({
                        "absent_identity": cu.identity,
                        "absent_municipality": cu.municipality,
                        "substitute_identity": cu.substitute.get_full_name(),
                    })
                elif (cu.presence == PresenceStatus.REPLACED and cu.alternate == cu.substitute) or cu.presence == PresenceStatus.UNREPLACED:
                    # 4/ Les absents excusés
                    excused.append(user_info)

            # print(colored("titulaires présents", "green"), colored(titulars, "white", "on_green"))
            # print(colored("suppléants présents", "green"), colored(alternates, "white", "on_green"))
            # print(colored("absents excusés avec procuration", "green"), colored(replaced, "white", "on_green"))
            # print(colored("absents excusés", "green"), colored(excused, "white", "on_green"))
            
            # Ajouter les listes au contexte
            context['titulars'] = titulars
            context['alternates'] = alternates
            context['replaced'] = replaced
            context['unreplaced'] = excused

        return context

    def compte_rendu_page_view(request, page_id):
        page = CompteRenduPage.objects.get(id=page_id)
        return page.serve_pdf(request)
    
    def get_template(self, request, *args, **kwargs):
        parent_page = self.get_parent().specific
        if isinstance(parent_page, CommissionPage):
            template_path = "administration/commissions/compte_rendu_page.html"
        else:
            parent_page_slug = parent_page.slug
            template_path = f"administration/{parent_page_slug}/compte_rendu_page.html"
        return template_path
    
    class Meta:
        verbose_name = "compte-rendu"
        verbose_name_plural = "comptes-rendus"

###############
##  WIDGETS  ##
############### 
        
# Liste de documents (convoc)
class ConvocationPieceJointe(PJBlock):
    """Modèle de pièce jointe spécifique à la ConvocationPage."""

    page = ParentalKey(
        ConvocationPage,
        on_delete=models.CASCADE,
        related_name="convocation_documents",
    )

# Liste de documents (cr)
class CompteRenduPieceJointe(PJBlock):
    """Modèle de pièce jointe spécifique à la CompteRenduPage."""

    page = ParentalKey(
        CompteRenduPage,
        on_delete=models.CASCADE,
        related_name="compte_rendu_documents",
    )

# Etat de présence
class PresenceStatus(models.IntegerChoices):
    PRESENT = 1, _('Présent')
    REPLACED = 2, _('Remplacé')
    UNREPLACED = 3, _('Non remplacé')

# Participations à une instance (Lié à une convocation puis, indirectement, à un compte-rendu)
class ConvocationUser(models.Model):
    convocation = models.ForeignKey('administration.ConvocationPage', on_delete=models.CASCADE, verbose_name=_("Convocation"), related_name='convocation_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    parent = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Parent Page"), related_name='convocation_user_parents')
    function_weight = models.IntegerField(verbose_name=_("Function Weight"), null=True, blank=True)
    function = models.CharField(max_length=255, verbose_name=_("Function"), blank=True, null=True)
    gender = models.CharField(max_length=50, verbose_name=_("Gender"), blank=True, null=True)
    identity = models.CharField(max_length=255, verbose_name=_("Identity"), blank=True, null=True)
    municipality = models.CharField(max_length=255, verbose_name=_("Municipality"), blank=True, null=True)
    presence = models.IntegerField(choices=PresenceStatus.choices, default=PresenceStatus.PRESENT, verbose_name=_("Presence"))
    substitute = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Substitute"), related_name='convocation_user_substitutes')
    alternate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Alternate"), related_name='convocation_user_alternates')
    
    api_fields = [
        APIField('id'),
        APIField('detail_url'),
        APIField('user'),
        APIField('parent'),
        APIField('parent_url'),
        APIField('function_weight'),
        APIField('function'),
        APIField('gender'),
        APIField('identity'),
        APIField('municipality'),
        APIField('presence'),
        APIField('substitute'),
        APIField('alternate'),
    ]
    
    search_fields = [
        index.SearchField('function'),
        index.SearchField('gender'),
        index.SearchField('identity'),
        index.SearchField('municipality'),
        index.FilterField('presence'),
        index.FilterField('function_weight'),
        index.RelatedFields('user', [
            index.SearchField('username'),
            index.SearchField('first_name'),
            index.SearchField('last_name'),
            index.SearchField('municipality'),
        ]),
        index.RelatedFields('substitute', [
            index.SearchField('username'),
            index.SearchField('first_name'),
            index.SearchField('last_name'),
            index.SearchField('municipality'),
        ]),
        index.RelatedFields('alternate', [
            index.SearchField('username'),
            index.SearchField('first_name'),
            index.SearchField('last_name'),
            index.SearchField('municipality'),
        ]),
    ]
    
    class Meta:
        unique_together = ('convocation', 'user')
        verbose_name = _("Convocation User")
        verbose_name_plural = _("Convocation Users")

    def __str__(self):
        return f"{self.identity} - {self.function}"

###############
## FONCTIONS ##
############### 

def cv_cr_filter(page, request):
    search_query = request.GET.get('query', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    type_filter = request.GET.get('type', 'all')
    
    convocations = ConvocationPage.objects.none()
    comptes_rendus = CompteRenduPage.objects.none()

    # Filtre conditionnel en fonction du type sélectionné
    if type_filter in ['all', 'convocations']:
        convocations = ConvocationPage.objects.live().descendant_of(page).order_by('date')
    if type_filter in ['all', 'comptes_rendus']:
        comptes_rendus = CompteRenduPage.objects.live().descendant_of(page).order_by('date')

    # Filtre conditionnel en fonction de la date sélectionnée
    if start_date:
        start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
        convocations = convocations.filter(date__gte=start_date)
        comptes_rendus = comptes_rendus.filter(date__gte=start_date)
    if end_date:
        end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
        convocations = convocations.filter(date__lte=end_date)
        comptes_rendus = comptes_rendus.filter(date__lte=end_date)

    # Filtre conditionnel en fonction de la recherche
    if search_query:
        search_backend = get_search_backend()
        convocations = search_backend.search(search_query, convocations)
        comptes_rendus = search_backend.search(search_query, comptes_rendus)

    # Regroupez et triez les pages par année
    convocation_pages_by_year = defaultdict(list)
    compterendu_pages_by_year = defaultdict(list)
    for convocation in convocations:
        convocation_pages_by_year[convocation.date.year].append(convocation)
    for compte_rendu in comptes_rendus:
        compterendu_pages_by_year[compte_rendu.date.year].append(compte_rendu)

    # Retourne les données triées et filtrées
    return {
        'convocation_pages_by_year': dict(convocation_pages_by_year),
        'compterendu_pages_by_year': dict(compterendu_pages_by_year),
    }
