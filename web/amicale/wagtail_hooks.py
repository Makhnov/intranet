import json
from wagtail import hooks
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.html import strip_tags
from django.core.mail import EmailMessage, send_mail
from utils.mailing import cgs_mail
from wagtailstreamforms.hooks import register, get_setting
from wagtailstreamforms.utils.requests import get_form_instance_from_request

# Envoir d'un email lors d'une soumission de formulaire
@register('process_form_submission')
def email_submission(instance, form):
    print(f'instance: {instance}')
    """ Send an email with the submission. """
    subject = f'New Form Submission from {instance.title}'
    message = "A new submission has been received. Here are the details:\n"
    message += "\n".join(f"{field}: {value}" for field, value in form.cleaned_data.items())
    from_email = 'intranet'
    recipient_list = ['lougarre.helene@cagiregaronnesalat.fr']

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

    # only process if settings.WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING is True
    if not get_setting('ENABLE_FORM_PROCESSING'):
        return
        
    if request.method == 'POST':
        form_def = get_form_instance_from_request(request)
                
        if form_def:
            form = form_def.get_form(request.POST, request.FILES, page=page, user=request.user)
            context = page.get_context(request)
            
            if form.is_valid():
                # process the form submission
                form_def.process_form_submission(form)
                
                # create success message
                if form_def.success_message:
                    # messages.success(request, strip_tags(str(page.thank_you_text)))
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
