from termcolor import colored
from taggit.models import Tag
from django import template
from datetime import timedelta
from django.utils import timezone

from utils.variables import FILE_EXTENSIONS
from utils.auth import check_page_access
from home.models import generic_search
from amicale.models import (
    AmicaleIndexPage, 
    AmicalePage,
    AmicaleInscriptionPage,    
)
from agents.models import (
    FaqIndexPage, 
    FaqCategory,
    FaqPage,
)
from administration.models import (
    AdministrationIndexPage, 
    AdministrationFormPage,
    ConseilsIndexPage, 
    BureauxIndexPage, 
    ConferencesIndexPage, 
    CommissionsIndexPage,
    CommissionPage, 
    ConvocationPage, 
    CompteRenduPage, 
    CommissionPage,
)

slugs = {
    "administration" : AdministrationIndexPage,
    "conseils" : ConseilsIndexPage,
    "bureaux" : BureauxIndexPage,
    "conferences" : ConferencesIndexPage,
    "commissions" : CommissionsIndexPage,
}

register = template.Library()

####################################################################################################
#########################                     GENERAUX                     #########################
#################################################################################################### 

@register.filter
def get_field(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def get_doc(page, doc):
    return getattr(page, f"{doc}_documents").all()

@register.filter(name='getlist')
def getlist(value, arg):
    return value.getlist(arg)

@register.filter(name='split')
def split(value, key):  
    value.split("key")
    return value.split(key)

@register.filter(name='replace')
def replace(value, args):
    search, replace = args.split(',')
    return value.replace(search, replace)

@register.filter(name='classname')
def classname(obj):
    return obj.__class__.__name__

@register.filter(name='spread')
def spread(value, delimiter):
    """
    Divise la chaîne autour de la première occurrence du délimiteur et retourne un tuple de deux éléments.
    """
    parts = value.split(delimiter, 1)  # Divise en deux parties au maximum
    if len(parts) == 2:
        return parts[0], parts[1]
    return value, ''

@register.filter(name='get_extension_info')
def get_extension_info(filename):
    ext = filename.split('.')[-1].lower()
    return FILE_EXTENSIONS.get(ext, ("unknown", "Type de fichier inconnu"))


####################################################################################################
#########################     RECHERCHE (filters.html et theme.html)       #########################
#################################################################################################### 

# FAQ THEMES
@register.inclusion_tag('agents/widgets/themes.html', takes_context=True)
def agents_themes(context, class_type=None, index=None):
    request = context['request']
    settings = context['settings']
    selected = request.GET.get('category', '')
    themes = FaqCategory.objects.all().order_by('title')
    page = context['page']
    delta = timezone.now() - timedelta(days=getattr(settings, "DELTA_NEWS", 30))
    new_faqs = {}
    news = 0
    
    for theme in themes:
        count = FaqPage.objects.filter(category=theme, latest_revision_created_at__gte=delta).count()
        new_faqs[theme.id] = count
        news += count

    return {
        'request': request,
        'settings': settings,
        'selected': selected,
        'themes': themes,
        'class_type': class_type,
        'index': index,
        'new': new_faqs,
        'news': news,    
        'page': page,
    }

# AMICALE THEMES
@register.inclusion_tag('amicale/widgets/themes.html', takes_context=True)
def amicale_themes(context, class_type=None, index=None):
    request = context['request']
    settings = context['settings']
    page = context['page']
    user = request.user
    
    # print(colored(f"Utilisateur: {user}", "yellow", 'on_black'))
    # print(colored(f"Amicale: {ami}", "yellow", 'on_black'))
    
    selected = request.GET.get('type', '')
    if isinstance(page, AmicaleInscriptionPage):
        selected = 'inscription'
        
    delta = timezone.now() - timedelta(days=getattr(settings, "DELTA_NEWS", 30))
    new_amicale = {}
    news = 0
    types = {
        'autres': 'Informations diverses',
        'sorties': 'Sorties',
        'inscription': 'Inscription à l\'amicale',
        'news': 'Nouvelles',
    }

    ami = user.groups.filter(name='Amicale').exists()    
    if ami:
        types.pop('inscription')

    for key, field in types.items():
        count = AmicalePage.objects.filter(type=key, latest_revision_created_at__gte=delta).count()
        new_amicale[key] = count
        news += count

    return {
        'request': request,
        'settings': settings,
        'selected': selected,
        'themes': types,
        'class_type': class_type,
        'index': index,
        'new': new_amicale,
        'news': news,
        'page': page,
        'ami': ami,
    }

# CLOUD (PAGES PUBLIQUES ET RESSOURCES)
@register.inclusion_tag('home/widgets/themes.html', takes_context=True)
def cgs_cloud(context, class_type=None, index=None):
    request = context['request']
    settings = context['settings']
    page = context['page']
    
    slug = page.slug  
    selected = request.GET.get('type', '')
    grouped_subpages, search_query, page_type = generic_search(request, context.get('page'))
    new_home = {}
    news = 0
    types = {
        'generic': 'Pages diverses',
        'download': 'Fichiers et téléchargements',
        'form': 'Formulaires',
    }
    
    for type_key in grouped_subpages:
        count = len(grouped_subpages[type_key])
        new_home[type_key] = count
        news += count

    return {
        'request': request,
        'settings': settings,
        'selected': selected,
        'item_type':slug,
        'themes': types,
        'class_type': class_type,
        'index': index,
        'new': new_home,
        'news': news,
        'page': page,
    }


####################################################################################################
#########################                     QUICKBAR                     #########################
####################################################################################################

# ADMINISTRATION QUICKBAR (prochaine convoc, dernier compte-rendu)
@register.inclusion_tag('administration/widgets/news.html', takes_context=True)
def administration_quickbar(context):
    request = context['request']
    user = request.user
    page = context['page']
    settings = context.get('settings', None)

    # print(colored(f"page: {page}", "yellow", 'on_black'))
    # print(colored(f"settings: {settings}", "yellow", 'on_black'))
    # print(colored(f"user: {user}", "yellow", 'on_black'))
    
    # Détermine les pages à partir desquelles filtrer les convocations et comptes rendus
    if isinstance(page, (CommissionPage, BureauxIndexPage, ConferencesIndexPage, ConseilsIndexPage)):
        pages = [page]
    else:
        pages = page.get_children().live().specific()

    # print(colored(f"pages: {pages}", "yellow", 'on_black')) 
    
    # Initialise les variables
    convocation = None
    compte_rendu = None

    # Boucle pour filtrer en fonction de l'accès utilisateur
    for pg in pages:
        # print(colored(f"pg: {pg}", "yellow", 'on_black'))
        if not isinstance(pg, AdministrationFormPage) and check_page_access(user, pg, False):
            # Récupère la prochaine convocation et le dernier compte-rendu
            next_convocations = ConvocationPage.objects.live().descendant_of(pg).filter(date__gte=timezone.now()).order_by('date').first()
            last_compte_rendus = CompteRenduPage.objects.live().descendant_of(pg).filter(date__lte=timezone.now()).order_by('-date').first()

            # Met à jour convocation et compte_rendu si nécessaire
            if next_convocations and (not convocation or next_convocations.date < convocation.date):
                convocation = next_convocations
            if last_compte_rendus and (not compte_rendu or last_compte_rendus.date > compte_rendu.date):
                compte_rendu = last_compte_rendus

    cv_parent = convocation.get_parent() if convocation else None
    cr_parent = compte_rendu.get_parent() if compte_rendu else None

    return {
        'convocation': convocation,
        'compte_rendu': compte_rendu,
        'cv_parent': cv_parent,
        'cr_parent': cr_parent,
        'settings': settings,
        'page': page,
    }

# AGENTS FAQ QUICKBAR (Les trois dernières FAQ)
@register.inclusion_tag('widgets/news/news.html', takes_context=True)
def agents_quickbar(context):
    settings = context.get('settings', None)
    request = context['request']
    category = request.GET.get('category', '')
    
    # on récupère l'ID de la catégorie en fonction de son nom
    if category and category != "*":
        category = FaqCategory.objects.get(slug=category).id
    else:
        category = "*"

    # on récupere les 3 dernières faq dont la catégorie est celle de la page (si "*" alors toutes les catégories)
    if category == "*":
        faqs = FaqPage.objects.live().order_by('-latest_revision_created_at')[:3]
    else:
        faqs = FaqPage.objects.live().filter(category=category).order_by('-latest_revision_created_at')[:3]   
     
    # print(colored(f"faq: {faqs}", "yellow", 'on_black'))
    
    # On crée un receptacle pour les contextes
    items = []
    
    for faq in faqs:
        # print(colored(f"faq: {faq}", "yellow", 'on_black'))
        name = faq.question
        # print(colored(f"name: {name}", "yellow", 'on_black'))
        url = faq.get_url()
        # print(colored(f"url: {url}", "yellow", 'on_black'))
        category = faq.category
        items.append({'item_type':'faq', 'name': name, 'url': url, 'category': category})
    
    return {'items': items, 'settings': settings}

# ADMINISTRATION QUICKBAR (prochaine convoc, dernier compte-rendu)
@register.inclusion_tag('widgets/news/news.html', takes_context=True)
def amicale_quickbar(context):
    settings = context.get('settings', None)
    
    # on récupere les sorties à venir (dont la date est plus lointaine que la date du jour)
    sorties = AmicalePage.objects.live().filter(type='sorties', date__gte=timezone.now()).order_by('date')[:3]
    # print(colored(f"sorties: {sorties}", "yellow", 'on_black'))
        
    items = []
    
    for sortie in sorties:        
        name = sortie.title
        # print(colored(f"name: {name}", "yellow", 'on_black'))
        url = sortie.get_url()
        # print(colored(f"url: {url}", "yellow", 'on_black'))        
        items.append({'item_type':'amicale', 'name': name, 'url': url, 'category': 'Sorties'})
    
    return {'items': items, 'settings': settings}
    