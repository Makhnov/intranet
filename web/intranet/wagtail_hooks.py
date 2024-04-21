from termcolor import colored

import json
import uuid
import itertools

# Wagtail
from wagtail import hooks
from wagtail.models import Page

# Amicale
from amicale.models import AmicaleInscriptionPage, AmicalePage

# Agents
from agents.models import FaqPage, FaqFormPage

# Dashboard
from dashboard.models import IntranetIcons

# Home
from home.models import InstantDownloadPage, HomeFormPage

# Mots-clefs :
from utils.variables import STOP_WORDS

# Traduction
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import pluralize

# Restrictions
from utils.auth import login_restricted_pages
from utils.variables import FILE_EXTENSIONS
from wagtail.models import PageViewRestriction

# Formulaires
from wagtailstreamforms.hooks import register, get_setting
from wagtailstreamforms.utils.requests import get_form_instance_from_request
from wagtailstreamforms.models import FormSubmissionFile, FormSubmission, Form
from wagtailstreamforms.serializers import FormSubmissionSerializer

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
    if len(attachments) > 1:
        # Gérer plusieurs fichiers attachés
        total_size = sum(attachment.document.file.size for attachment in attachments)
        file_descriptions = []
        file_types = []
        
        for attachment in attachments:
            document = attachment.document if attachment else None
            if document:
                extension = document.filename.split(".")[-1]
                prefix = attachment.title if attachment.title else document.title if document.title else document.filename if document.filename else "Document inconnu"
                prefix = prefix[:15] + ("..." if len(prefix) > 15 else "")
                
                if extension in FILE_EXTENSIONS:
                    file_type, file_desc = FILE_EXTENSIONS[extension]
                    if prefix not in file_descriptions:
                        file_descriptions.append(prefix)
                    file_types.append(f"{file_type}_file")

        # Construire le titre, le heading et le tooltip pour multiples fichiers
        prefix = ', '.join(file_descriptions[:3]) + (", etc." if len(file_descriptions) > 3 else "")
        midfix = f"{round(total_size / 1000000, 2)} Mo"
        suffix = f"{len(file_descriptions)} fichiers"
        new_title = f"[{prefix}]-[{midfix}]-[{suffix}]"
        new_heading = 'archive_file, '
        new_heading += ', '.join(file_types)
        new_tooltip = "Télécharger les fichiers"
        
        # Récupérer le logo pour 'archive_file'
        icons = IntranetIcons.for_site(page.get_site())
        icon = getattr(icons, "archive_file", None)

    else:
        # Gérer un seul fichier attaché (logique d'origine)
        document = attachments[0].document if attachments else None
        if document:
            prefix = attachments[0].title if attachments[0].title else document.title if document.title else document.filename if document.filename else "Document inconnu"
            prefix = prefix[:20] + ("..." if len(prefix) > 20 else "")
            extension = document.filename.split(".")[-1]
            suffix = f"{round(document.file.size / 1000)} Ko" if document.file.size < 100000 else f"{round(document.file.size / 1000000, 2)} Mo"
            if extension in FILE_EXTENSIONS:
                file_type, file_desc = FILE_EXTENSIONS[extension]
                new_title = f"[{prefix}]-[{file_desc if file_desc else 'inconnu'}]-[{suffix}]"
                new_heading = f"{file_type}_file"
                new_tooltip = f"Télécharger {prefix}"
                icons = IntranetIcons.for_site(page.get_site())
                icon = getattr(icons, f"{file_type}_file", None)
            else:
                new_title = f"[{prefix}]-[{suffix}]"
                new_heading = "unknown_file"
                new_tooltip = "Télécharger document"
                icon = None
        else:
            new_title = "Document inconnu"
            new_heading = "unknown_file"
            new_tooltip = "Télécharger document"
            icon = None

    # Appliquer les changements
    if page.title != new_title or page.heading != new_heading or page.tooltip != new_tooltip or page.logo != icon:
        page.title = new_title
        page.heading = new_heading
        page.tooltip = new_tooltip
        if icon:
            page.logo = icon
        page.save()
        page.specific.save()
        page.save_revision().publish()

            
#####################################################################################################################################################################################
#                                                                           ENVOI DE MAILS (FORMULAIRES)                                                                            #
#####################################################################################################################################################################################  

# ETAPE 0 et 2 : On ajoute les champs cachés (origine et utilisateur) au formulaire (Ils ont été préalablement ajoutés lors de la construction HTML de la page)
@register('construct_submission_form_fields')
def add_form_fields(form_fields):
    """ Prépare les champs custom pour la soumissions :
    - utilisateur pour vérifier les doublons d'envoi
    - origine pour connaitre la page d'origine de l'envoi
    """
    # print(colored(f'#Etape 0/2 : Ajout de champs spécifiques:', 'red', 'on_white'))
    # print(colored('...', 'white', 'on_red'))
    
    form_fields.append({
        "id": str(uuid.uuid4()),
        "type": "hidden",
        "value": {
            "label": "Origine",
            "required": False,
            "help_text": "",
            "default_value": "Page inconnue"
        }
    })
    form_fields.append({
        "id": str(uuid.uuid4()),
        "type": "hidden",
        "value": {
            "label": "Userid",
            "required": False,
            "help_text": "",
            "default_value": "Utilisateur inconnu"
        }
    })
    return form_fields


# ETAPE 1 : On vérifie si le formulaire est valide
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
    elif isinstance(page, AmicalePage):        
        if not user.groups.filter(name='Amicale').exists():
            messages.warning(request, _('You have to be an amicale member to sign in for this event. Hopefully you can click on the 📝 in the top right corner to sign up.'), fail_silently=True)            
            return redirect(f'{page.get_url(request)}?inscription=true')        
    elif isinstance(page, FaqFormPage):
        pass
    elif isinstance(page, HomeFormPage):
        pass
    
    if not get_setting('ENABLE_FORM_PROCESSING'):        
        messages.warning(request, _('Form processing is disabled.'), fail_silently=True)
        return redirect('/amicale/')          
    
    # print(colored(f'#Etape 1 : Il s\'agit bien d\'un formulaire wagtail : {form_def.id} // Page : {page}', 'red', 'on_white'))
    # print(colored('...', 'white', 'on_red'))
        
    if hasattr(form_def.advanced_settings, 'unique'):
        unique = form_def.advanced_settings.unique
                
    if unique:
        if form_def.get_submission_class().objects.filter(form_id= form_def.id, form_data__contains=f'"userid": "{user.id}"').exists():
            print(colored('Un doublon existe déjà pour cet utilisateur et ce formulaire.', 'red'))
            messages.warning(request, _('You have already submitted this form.'), fail_silently=True)
            return redirect('/amicale/')
    
    form = form_def.get_form(request.POST, request.FILES, page=page, user=request.user)
    context = page.get_context(request)
        
    if form.is_valid():
        form_def.process_form_submission(form)
        # print(colored(f'#Etape 5 fin du traitement...', 'red', 'on_white'))
        
        # create success message
        if form_def.success_message:
            messages.success(request, form_def.success_message, fail_silently=True)                   
        else:
            messages.success(request, 'Votre demande a bien été enregistrée.', fail_silently=True)
            
        redirect_page = form_def.post_redirect_page or page.get_parent()
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
        else:
            messages.error(request, 'Une erreur est survenue lors de l\'envoi du formulaire.', fail_silently=True)
        # On retourne la page avec le formulaire invalide  
        return TemplateResponse(
            request,
            page.get_template(request, *args, **kwargs),
            context
        )


@register("process_form_submission")
def save_form_submission_data(instance, form):
    """ Sauvegarde les données du formulaire. """    
    # print(colored(f'#Etape 3 : Sauvegarde des données: {instance}', 'red', 'on_white')) 
    # print(colored('...', 'white', 'on_red'))
       
    # Copier les données nettoyées pour ne pas interférer avec l'original
    submission_data = form.cleaned_data.copy()
    # print(colored(f'submission: {submission_data}', 'cyan'))
    
    # print les files et les files keys
    # print(colored(f'files: {form.files}', 'cyan'))
    # print(colored(f'files keys: {form.files.keys()}', 'cyan'))
    
    # changer les données de soumission en un compteur des fichiers
    for field in form.files.keys():
        print(colored(f'field: {field}', 'cyan', 'on_white'))
        count = len(form.files.getlist(field))
        submission_data[field] = "{} file{}".format(count, pluralize(count))
        
    # sauvegarder les données de soumission
    submission = instance.get_submission_class().objects.create(
        form_data=json.dumps(submission_data, cls=FormSubmissionSerializer),
        form=instance,
    )
    # print(colored(f'Real submission: {submission}', 'green'))
    
    # sauvegarder les fichiers du formulaire
    for field in form.files:
        for file in form.files.getlist(field):
            FormSubmissionFile.objects.create(submission=submission, field=field, file=file)
            print(colored(f'file: {file}', 'cyan'))
    
    return submission


# Envoir d'un email lors d'une soumission de formulaire
@register('process_form_submission')
def email_submission(instance, form):
    """ Envoie un email lorsqu'un formulaire est soumis. """
    # print(colored(f'#Etape 4 : Envoie de mail: {instance}', 'red', 'on_white'))
    # print(colored('...', 'white', 'on_red'))
    
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
