from termcolor import colored
from wagtail import hooks

# Amicale
from amicale.models import AmicaleInscriptionPage

# Agents
from agents.models import FaqPage

# Home
from home.models import InstantDownloadPage

# Mots-clefs :
from utils.variables import STOP_WORDS

# Traduction
from django.utils.translation import gettext_lazy as _

# Restrictions
from utils.auth import login_restricted_pages
from utils.variables import extensions
from wagtail.models import PageViewRestriction

# Formulaires
from wagtailstreamforms.hooks import register, get_setting
from wagtailstreamforms.utils.requests import get_form_instance_from_request
from wagtailstreamforms.models import FormSubmission, Form

# Mailing
from utils.mailing import cgs_mail
from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render
from django.contrib import messages

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
#                                                                           ENVOI DE MAILS (FORMULAIRES)                                                                            #
#####################################################################################################################################################################################  

# Envoir d'un email lors d'une soumission de formulaire
@register('process_form_submission')
def email_submission(instance, form):
    print(f'instance: {instance}')
    """ Send an email with the submission. """
    
    # Sujet du mail
    subject = f'New Form Submission from {instance.title}'
    if hasattr(instance.advanced_settings, 'subject'):
        subject = f'{instance.advanced_settings.subject} - {instance.title}'
    
    # Message du mail
    message = "Un formulaire a été validé, en voici les détails:\n"
    message += "\n".join(
        f"{field}: {'Validé' if value is True else 'Non validé' if value is False else 'Aucun(e)' if value is None else value}"
        for field, value in form.cleaned_data.items()
        if field not in ['form_id', 'form_reference']
    )
   
    # Expéditeur (Les adresses sont toujours en @cagiregaronnesalat.fr)
    from_email = 'intranet'
 
    # Destinataire(s)
    adress = settings.WAGTAILSTREAMFORMS_DEFAULT_TO_ADDRESS
    if hasattr(instance.advanced_settings, 'to_address'):
        adress = instance.advanced_settings.to_address    
    recipient_list=[adress]

    # Préparation des pièces jointes
    fichiers = {}
    for field in form.files:
        for file in form.files.getlist(field):
            file.seek(0)  # Rebobiner le fichier au cas où
            fichiers[file.name] = file.read()

    # Utilisation de cgs_mail pour envoyer le mail avec les pièces jointes
    cgs_mail(subject, message, from_email, recipient_list, fichiers=fichiers)


@hooks.register('before_serve_page')
def custom_process_form(page, request, *args, **kwargs): 
    """ Process the form if there is one, if not just continue. """

    if request.method != 'POST':
        return   
    
    form_def = get_form_instance_from_request(request)
    if form_def is None:
        return
    
    if not isinstance(form_def, Form):
        return
    
    user = request.user
    unique = False

    # print(colored(f'Is instance: {isinstance(page, AmicaleInscriptionPage)}', 'cyan'))
    # print(colored(f'User is amicale member : {user.groups.filter(name="Amicale").exists()}', 'cyan'))
    
    if isinstance(page, AmicaleInscriptionPage):
        if user.groups.filter(name='Amicale').exists():
            messages.warning(request, _('You are already an amicale member.'), fail_silently=True)
            return redirect('/amicale/')
        
    if not get_setting('ENABLE_FORM_PROCESSING'):        
        messages.warning(request, _('Form processing is disabled.'), fail_silently=True)
        return redirect('/amicale/')          
    
    if hasattr(form_def.advanced_settings, 'unique'):
        unique = form_def.advanced_settings.unique
                
    if unique:
        if user_has_already_submitted(user, form_def.id):
            messages.warning(request, _('You have already submitted this form.'), fail_silently=True)
            return redirect('/amicale/')
    
    # print(colored(f'form_def is an instance of Form. ID : {form_def.id} // Page : {page}', 'cyan'))

    form = form_def.get_form(request.POST, request.FILES, page=page, user=request.user)
    context = page.get_context(request)
        
    if form.is_valid():
        # process the form submission
        form_def.process_form_submission(form)
        
        # create success message
        if form_def.success_message:
            messages.success(request, form_def.success_message, fail_silently=True)                   

        # return redirect('/amicale/')
        redirect_page = form_def.post_redirect_page or page
        return redirect(redirect_page.get_url(request), context=context)                   
    else:
        # update the context with the invalid form and serve the page
        context.update({
            'invalid_stream_form_reference': form.data.get('form_reference'),
            'invalid_stream_form': form
        })
        
        # create error message
        if form_def.error_message:
            messages.error(request, form_def.error_message, fail_silently=True)
            
        return TemplateResponse(
            request,
            page.get_template(request, *args, **kwargs),
            context
        )

def user_has_already_submitted(user, form_id):
    """Vérifie si un utilisateur a déjà soumis une réponse pour un formulaire spécifique."""
    has_submitted = FormSubmission.objects.filter(
        form__id=form_id
    ).exists()
    
    return has_submitted
