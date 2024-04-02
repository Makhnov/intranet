from taggit.models import Tag
from django import template
from django.utils.timezone import now

from utils.auth import check_page_access
from agents.models import (
    FaqIndexPage, 
    FaqCategory
)
from administration.models import (
    AdministrationIndexPage, 
    ConseilsIndexPage, 
    BureauxIndexPage, 
    ConferencesIndexPage, 
    CommissionsIndexPage,
    CommissionPage, 
    ConvocationPage, 
    CompteRenduPage, 
    CommissionPage
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

####################################################################################################
#########################                        FAQ                       #########################
#################################################################################################### 

# FAQ INDEX
@register.simple_tag
def get_faq_index():
    faq_page = FaqIndexPage.objects.live().first()
    return faq_page

# FAQ TAGS
@register.inclusion_tag('agents/widgets/tags.html', takes_context=True)
def faq_tags(context, class_type=None, index=None):
    request = context['request']
    settings = context['settings']
    tags = Tag.objects.all().order_by('title')
    selected = request.GET.get('tag', '')
    return {
        'request': request,
        'settings':settings,
        'selected': selected,
        'tags': tags,
        'class_type': class_type,
        'index': index,
}
    
# FAQ THEMES
@register.inclusion_tag('agents/widgets/themes.html', takes_context=True)
def faq_themes(context, class_type=None, index=None):
    request = context['request']
    settings = context['settings']
    selected = request.GET.get('category', '')
    themes = FaqCategory.objects.all().order_by('title')
    return {
        'request': request,
        'settings':settings,
        'selected': selected,
        'themes': themes,
        'class_type': class_type,
        'index': index,
    }
    
# REQUEST LIST
@register.filter(name='getlist')
def getlist(value, arg):
    return value.getlist(arg)

# # FILTRES (TAGS, CATEGORIES)
# @register.filter
# def without(querystring, parameter):
#     """Returns the URL parameters without the specified parameter."""
#     query = QueryDict(querystring, mutable=True)
#     query.pop(parameter, None)
#     return query.urlencode()

####################################################################################################
#########################                  ADMINISTRATION                  #########################
####################################################################################################

# ADMINISTRATION QUICKBAR (prochaine convoc, dernier compte-rendu)
@register.inclusion_tag('administration/widgets/cv_cr.html', takes_context=True)
def cv_cr(context):
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
        if check_page_access(user, pg, False):
            # Récupère la prochaine convocation et le dernier compte-rendu
            next_convocations = ConvocationPage.objects.live().descendant_of(pg).filter(date__gte=now()).order_by('date').first()
            last_compte_rendus = CompteRenduPage.objects.live().descendant_of(pg).filter(date__lte=now()).order_by('-date').first()

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
    }

