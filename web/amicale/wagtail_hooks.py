from termcolor import colored

from utils.mailing import cgs_mail
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, render
from django.contrib import messages

from wagtailstreamforms.hooks import register, get_setting
from wagtailstreamforms.utils.requests import get_form_instance_from_request
from wagtailstreamforms.models import FormSubmission, Form
from amicale.models import AmicaleInscriptionPage
from wagtail import hooks

# Envoir d'un email lors d'une soumission de formulaire
@register('process_form_submission')
def email_submission(instance, form):
    print(f'instance: {instance}')
    """ Send an email with the submission. """
    subject = f'New Form Submission from {instance.title}'
    message = "A new submission has been received. Here are the details:\n"
    message += "\n".join(f"{field}: {value}" for field, value in form.cleaned_data.items())
    from_email = 'intranet'
    
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
