from termcolor import colored
from wagtail import hooks
from wagtail.models import PageViewRestriction

# Agents
from agents.models import FaqPage

# Home
from home.models import InstantDownloadPage

# Mots-clefs :
from utils.variables import STOP_WORDS

# Pages auto restreintes (Utilisateurs connectés uniquement)
from utils.auth import login_restricted_pages
from utils.variables import extensions

#####################################################################################################################################################################################
#                                                                                AFTER CREATE HOOKS                                                                                 #
#####################################################################################################################################################################################
@hooks.register("after_edit_page")
@hooks.register("after_create_page")
def after_edit_create_page(request, page):
    page_specific = page.specific
    if isinstance(page_specific, tuple(login_restricted_pages)):
        print(f'Applying view restriction to page {page}')
        apply_specified_page_restriction(page_specific)        
    if isinstance(page_specific, FaqPage):
        print(f'Updating defaults for page {page}')
        update_faq_page_defaults(page_specific)
    elif isinstance(page_specific, InstantDownloadPage):
        print(f'Updating defaults for page {page}')
        update_download_page_defaults(page_specific)
        
# AmicaleIndexPage, RessourcesPage, AccountPage, ProfilePage, LogoutPage, EmailPage, PasswordPage, PasswordResetPage, PasswordChangePage, PasswordSetPage
def apply_specified_page_restriction(page):
    # On vérifie si il existe une restriction
    existing_restrictions = PageViewRestriction.objects.filter(page=page)
    if not existing_restrictions.exists():
        # Restriction d'accès aux utilisateurs connectés
        PageViewRestriction.objects.create(
            page=page,
            restriction_type=PageViewRestriction.LOGIN
        )   

# FaqPage
def update_faq_page_defaults(page): 
    # Extrait la thématiques
    category = str(page.category)
    # Extrait les mots-clés importants de la question
    important_words = [
        word for word in page.question.split() if word.lower() not in STOP_WORDS
    ]    
    # Concatène les mots-clés (Si aucun : " ? ")
    key_words = " ? " if not important_words else " … ".join(important_words[:3])
    # Construit le nouveau titre
    new_title = f"[{category}] - [{key_words}]"
    # Créé le nouveau slug à partir de l'ID de la page
    new_slug = f"faq{page.id}"
    # Sauvegarde de la page uniquement si le titre ou le slug ont été modifiés
    if page.title != new_title or page.slug != new_slug:
        page.title = new_title
        page.slug = new_slug
        page.save(update_fields=["title", "slug"])
        page.specific.save()
        page.save_revision().publish()
        
# InstantDownloadPage
def update_download_page_defaults(page):
    attachments = page.download_documents.all()
    if attachments:
        document = attachments[0].document
        
        if attachments[0].title:
            prefix = attachments[0].title
            extension = document.filename.split(".")[-1]
        elif document.title:
            prefix = document.title
            extension = document.filename.split(".")[-1]
        else:
            prefix = document.filename 
            
        # Arrondir le sufixe en Ko si < 100000 octets en Mo sinon
        sufix = f"{round(document.file.size / 1000)} Ko" if document.file.size < 100000 else f"{round(document.file.size / 1000000, 2)} Mo"
    else:
        prefix = "Document"
        sufix = "inconnu"
        
    print(colored(f"extension: {extension}", "yellow"))
    
    if extension in extensions:
        extension = extensions[extension]
        print(colored(f"extension: {extension}", "cyan"))
        new_title = f"[{prefix}]-[{extension if extension else 'inconnu'}]-[{sufix}]"  
    else:
        new_title = f"[{prefix}]-[{sufix}]"
    
    new_slug = f"document{page.id}"
    if page.slug != new_slug or page.title != new_title:
        page.slug = new_slug
        page.title = new_title
        page.save()
        page.specific.save()
        page.save_revision().publish()
            
#####################################################################################################################################################################################        