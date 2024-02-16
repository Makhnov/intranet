from itertools import groupby

from django import forms
from django.db import models

from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    PageChooserPanel,
    MultiFieldPanel,
)

# Parentalkey 
from modelcluster.fields import ParentalKey

# Page de menu
from utils.menu_pages import MenuPage, menu_page_save

# Custom panels
from home.views import custom_content_panels, custom_promote_panels

# Tables de fonctions utilisateurs
from users.models import (
    FonctionsConseilListe, 
    FonctionsBureauListe, 
    FonctionsConferenceListe, 
    FonctionsCommissionListe
)

# Tables
from wagtail.contrib.table_block.blocks import TableBlock

# Medias, PJ, MenuPage
from home.models import MediaBlock, PiecesJointes

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

# Liste de choix pour CommissionPage
TYPE_CHOICES = [
    ('commission', 'Commission'),
    ('groupe_de_travail', 'Groupe de travail'),
]

from collections import defaultdict

from django.utils.timezone import make_aware
from datetime import datetime
from wagtail.search.backends import get_search_backend

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


# La page d'accueil de la partie administration du site
class AdministrationIndexPage(MenuPage):
    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "administration.ConseilsIndexPage",
        "administration.BureauxIndexPage",
        "administration.CommissionsIndexPage",
        "administration.ConferencesIndexPage",
    ]
    save = menu_page_save('administration')


# La page d'index des conseils
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
        members = User.objects.filter(function_council__isnull=False)
        members_sorted = {}
        for choice in FonctionsConseilListe.choices:
            code, label = choice
            members_sorted[label] = members.filter(function_council=code)
        return members_sorted
    
    def get_context(self, request):
        context = super().get_context(request)
        context['children'] = cv_cr_filter(self, request)
        context['members'] = self.get_members()
        return context
        
    class Meta:
        verbose_name = "conseil"
        verbose_name_plural = "conseils"


# La page d'index des bureaux
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
        members = User.objects.filter(function_council__isnull=False)
        members_sorted = {}
        for choice in FonctionsBureauListe.choices:
            code, label = choice
            members_sorted[label] = members.filter(function_council=code)
        return members_sorted


    def get_context(self, request):
        context = super().get_context(request)
        context['children'] = cv_cr_filter(self, request)
        context['members'] = self.get_members()
        return context
    
    class Meta:
        verbose_name = "bureau"
        verbose_name_plural = "bureaux"


# La page d'index des commissions
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
        members = User.objects.filter(function_council__isnull=False)
        members_sorted = {}
        for choice in FonctionsConferenceListe.choices:
            code, label = choice
            members_sorted[label] = members.filter(function_council=code)
        return members_sorted
        
    
    def get_context(self, request):
        context = super().get_context(request)
        context['children'] = cv_cr_filter(self, request)
        context['members'] = self.get_members()
        return context
    
    class Meta:
        verbose_name = "conférence"
        verbose_name_plural = "conférences"


# La liste de toutes les commissions
class CommissionsIndexPage(MenuPage):
    parent_page_types = ["administration.AdministrationIndexPage"]
    subpage_types = ["administration.CommissionPage"]
    save = menu_page_save('commissions')

    class Meta:
        verbose_name = "Commissions (Index)"


# La page d'index d'une commission ou d'un groupe de travail
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
        members = User.objects.filter(commission=self)

        members_sorted = {}
        for choice in FonctionsCommissionListe.choices:
            code, label = choice
            members_sorted[label] = members.filter(function_commission=code)
        
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

 
# Page de convocation
class ConvocationPage(PdfViewPageMixin, Page):
    parent_page_types = [
        "administration.ConseilsIndexPage",
        "administration.BureauxIndexPage",
        "administration.CommissionPage",
        "administration.ConferencesIndexPage",
    ]
    show_in_menus_default = True
    template_name = "administration/conseils/convocation_page.html"
    admin_template_name = "administration/conseils/convocation_page.html"
    ROUTE_CONFIG = [
        ("html", r'^$'),
        ("pdf", r'^pdf/$'),
    ]
    
    date = models.DateTimeField(verbose_name="Date")
    body = RichTextField(blank=True, verbose_name=_("Agenda"))

    content_panels = custom_content_panels(["title"]) + [
        FieldPanel("date"),
        FieldPanel("body"),
        InlinePanel(
            "convocation_documents",
            label=_("Document"),
            heading=_("Attachments"),
            classname="collapsible collapsed",
        ),
    ]
    promote_panels = custom_promote_panels(["slug"])
        
    api_fields = [   
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
        if not self.title:  # Si le titre n'est pas déjà défini
            self.title = "convocation"
        if not self.slug:  # Si le slug n'est pas déjà défini
            self.slug = "convocation"
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

        # Récupération et tri des utilisateurs par poids de fonction puis par fonction
        convocation_users = ConvocationUser.objects.filter(
            convocation=self
        ).order_by('function_weight', 'function')

        # Regroupement des utilisateurs par fonction
        grouped_convocation_users = {
            k: list(g) for k, g in groupby(convocation_users, lambda x: x.function)
        }

        context['grouped_convocation_users'] = grouped_convocation_users
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

       
# Page de compte-rendu
class CompteRenduPage(PdfViewPageMixin, Page):
    parent_page_types = [
        "administration.ConseilsIndexPage",
        "administration.BureauxIndexPage",
        "administration.CommissionPage",
        "administration.ConferencesIndexPage",
    ]
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
        help_text=_("Uncheck this box if the quorum isn't reached."),
    )
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title", icon="title")),
            ("paragraph", blocks.RichTextBlock(icon="pilcrow")),
            ("media", MediaBlock(icon="media")),
            ("image", ImageChooserBlock(icon="image")),
            ("link", blocks.URLBlock(icon="link")),
            ("embed", EmbedBlock(icon="media")),
            (
                "list",
                blocks.ListBlock(blocks.CharBlock(icon="list-ul"), icon="list-ul"),
            ),
            ("quote", blocks.BlockQuoteBlock(icon="openquote")),
            ("table", TableBlock(icon="table")),
        ],
        use_json_field=True,
        blank=True,
        null=True,
        verbose_name=_("Agenda"),
        help_text=_("This is the main content of the page."),
    )

    content_panels = custom_content_panels(["title"]) + [
        PageChooserPanel("convocation", "administration.ConvocationPage"),
        FieldPanel(
            "secretary",
            widget=forms.Select,
        ),
        FieldPanel(
            "replaced_users", 
            widget=forms.CheckboxSelectMultiple,
        ),
        FieldPanel(
            "unreplaced_users", 
            widget=forms.CheckboxSelectMultiple,
        ),
        FieldPanel("date", read_only=True),
        FieldPanel("quorum"),
        FieldPanel("body"),
        InlinePanel(
            "compterendu_documents",
            label=_("Document"),
            heading=_("Attachments"),
            classname="collapsible collapsed",
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
           
    def get_context(self, request, **kwargs):
        context = super().get_context(request, **kwargs)

        # Assurez-vous que la page a une convocation associée
        if self.convocation is not None:
            convocation_users = ConvocationUser.objects.filter(
                convocation=self.convocation
            ).select_related('user', 'substitute', 'alternate').order_by('function_weight')

            # Initialisation des listes pour les différentes catégories
            titulaires_presents = []
            suppléants_presents = []
            absents_excusés_avec_procuration = []
            absents_excusés = []

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
                    titulaires_presents.append(user_info)
                elif cu.alternate and cu.alternate == cu.substitute:
                    # 2/ Les suppléants présents
                    suppléants_presents.append({
                        "identity": cu.alternate.get_full_name(),
                        "municipality": cu.alternate.get_municipality_display(),
                    })
                    # Ajoute également le titulaire à la liste des absents excusés
                    absents_excusés.append(user_info)
                elif cu.presence == PresenceStatus.REPLACED and cu.alternate != cu.substitute:
                    # 3/ Les absents excusés ayant donné procuration
                    absents_excusés_avec_procuration.append({
                        "absent_identity": cu.identity,
                        "absent_municipality": cu.municipality,
                        "substitute_identity": cu.substitute.get_full_name(),
                    })
                elif (cu.presence == PresenceStatus.REPLACED and cu.alternate == cu.substitute) or cu.presence == PresenceStatus.UNREPLACED:
                    # 4/ Les absents excusés
                    absents_excusés.append(user_info)

            # Tri des titulaires par leur fonction
            titulaires_presents.sort(key=lambda x: x['function_weight'])
            # Ajouter les listes au contexte
            context['titular'] = titulaires_presents
            context['alternate'] = suppléants_presents
            context['replaced'] = absents_excusés_avec_procuration
            context['unreplaced'] = absents_excusés

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

        
# Liste de documents (convoc)
class ConvocationPieceJointe(PiecesJointes):
    """Modèle de pièce jointe spécifique à la ConvocationPage."""

    page = ParentalKey(
        ConvocationPage,
        on_delete=models.CASCADE,
        related_name="convocation_documents",
    )


# Liste de documents (cr)
class CompteRenduPieceJointe(PiecesJointes):
    """Modèle de pièce jointe spécifique à la CompteRenduPage."""

    page = ParentalKey(
        CompteRenduPage,
        on_delete=models.CASCADE,
        related_name="compterendu_documents",
    )


# Lien entre une convocation et ses utilisateurs # Etat de présence
class PresenceStatus(models.IntegerChoices):
    PRESENT = 1, _('Présent')
    REPLACED = 2, _('Remplacé')
    UNREPLACED = 3, _('Non remplacé')


# La table de lien
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
        APIField('function'),
        APIField('function_weight'),
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