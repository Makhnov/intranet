from django.db import models
from django.conf import settings
from django.utils.timezone import datetime

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# Traduction
from django.utils.translation import gettext_lazy as _

# Documents
from wagtail.documents.models import Document

# Recherche
from wagtail.search import index

# API
from wagtail.api import APIField

# TITRES ET SLUGS FIXES POUR LES PAGES DE MENU UNIQUES (Page de menu non concernée : home.InstantDownloadPage)
MENU_PAGE_TITLES = {
    # HOME
    'accueil':              'Intranet 3CGS',                        # home.HomePage
    'public':               'Pages publiques',                      # home.PublicPage
    'ressources':           'Ressources internes',                  # home.ResourcesPage
    
    # ADMINISTRATION
    'administration':       'Élus du Cagire',                       # administration.AdministrationIndexPage
    'conseils':             'Conseils communautaires',              # administration.ConseilsIndexPage
    'bureaux':              'Bureaux communautaires',               # administration.BureauxIndexPage
    'commissions':          'Commissions et groupes de travail',    # administration.CommissionsIndexPage
    'conferences':          'Conférences des maires',               # administration.ConferencesIndexPage
    
    # AGENTS
    'agents':               'Agents (FAQ)',                         # agents.FaqIndexPage

    # AMICALE
    'amicale':              'Amicale',                              # amicale.AmicaleIndexPage
    
    # ACCOMPTE
    'accompte':             'Compte utilisateur',                             # accompte.AccountPage
    'profil':               'Profil du compte',                     # accompte.ProfilePage
    'connexion':            'Connexion',                            # accompte.LoginPage
    'deconnexion':          'Déconnexion',                          # accompte.LogoutPage
    'inscription':          'Inscription',                          # accompte.SignupPage
    'mdp':                  'Mot de passe',                         # accompte.PasswordPage
    'mel':                  'Adresse email',                        # accompte.EmailPage
    'mdp_recup':            'Récupération du mot de passe',         # accompte.PasswordResetPage
    'mdp_init':             'Initialisation du mot de passe',       # accompte.PasswordSetPage
    'mdp_modif':            'Modification du mot de passe',         # accompte.PasswordChangePage
}

MENU_PAGE_SLUGS = {
    # HOME
    'accueil':              'home',
    'public':               'public',
    'ressources':           'ressources',
    
    # ADMINISTRATION
    'administration':       'administration',
    'conseils':             'conseils',
    'bureaux':              'bureaux',
    'commissions':          'commissions',
    'conferences':          'conferences',
    
    # AGENTS
    'agents':               'faq',
    
    # AMICALE
    'amicale':              'amicale',
    
    # ACCOMPTE
    'accompte':             'account',
    'profil':               'profile',
    'connexion':            'login',
    'deconnexion':          'logout',
    'inscription':          'signup',
    'mdp':                  'password',
    'mel':                  'email',
    'mdp_recup': 'reset',
    'mdp_init':   'set',
    'mdp_modif':     'change',
}

def menu_page_save(key):
    def save(self, *args, **kwargs):
        self.title = MENU_PAGE_TITLES[key]
        self.slug = MENU_PAGE_SLUGS[key]
        super(MenuPage, self).save(*args, **kwargs)
    return save

# Page de menu (abstract)
class MenuPage(Page):
    show_in_menus_default = True
    max_count = 1

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

    # Panneau de contenu
    content_panels = [
        FieldPanel(
            'title', 
            read_only=True,
            help_text=_("Title of the page, automaticaly generated, cannot be changed."),
        ),
        MultiFieldPanel([
                FieldPanel("logo"),
                FieldPanel("heading"),
                FieldPanel("tooltip"),
            ],
            heading=_("Menu display options (click to expand)"),
            help_text=_("Choose an icon and a tooltip to display on the index pages. Both optional, if none, CGS logo will be the icon and tooltip will refer as the page title"),
            classname="collapsible, collapsed",
        ),
    ]   
    
    # Panneau de promotion
    promote_panels = [
        FieldPanel(
            'slug', 
            read_only=True,
            help_text=_("Slug of the page, automaticaly generated, cannot be changed."),
        ),        
        FieldPanel(
            'show_in_menus',
            help_text=_("Uncheck to hide this page from the menus."),
        ),
    ]
       
    search_fields = Page.search_fields + [
        index.SearchField("heading"),
    ]    
    
    api_fields = [
        APIField("tooltip"),
        APIField("heading"),
        APIField("logo"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        menu_pages = getattr(settings, "WAGTAIL_MENU_PAGES", [])    
        admin_page = Page.objects.get(slug="administration")    
        commissions_index_page = Page.objects.get(slug="commissions")
        context['is_menu'] = self.__class__.__name__ in menu_pages
        context['menu_type'] = self.slug
        context['admin_menu'] = admin_page.get_children().live()
        context['commissions_menu'] = commissions_index_page.get_children().live()
        context['children'] = self.get_children().live()
        
        print(context)
        return context
    
    class Meta:
        abstract = True
