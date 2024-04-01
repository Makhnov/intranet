from termcolor import colored
import random
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from wagtail.admin import messages
from wagtail.models import Page
from mailing.forms import EmailForm
from utils.mailing import EmailSender
from django.utils import formats
from django.utils import translation
translation.activate('fr-fr')

@permission_required('mailing.can_send_mail', raise_exception=True)
def mailing_view(request):
    pages = Page.objects.live().specific()
    form = EmailForm(request.POST or None)
    if request.method == 'POST':        
        if form.is_valid():
            try:
                email_sender = EmailSender(request.user)
                data = form.cleaned_data
                left_pages = data.get('left_pages', None)
                right_pages = data.get('right_pages', None)
                main_page = None
                parent_page = None
                page_url = None
                attachments = data.get('left_attachments', False) or data.get('right_attachments', False)
                destinataires = data.get('mail_to', [])
                email_data = []

                if left_pages:
                    print(colored('left_pages', 'green'), colored(left_pages, 'white', 'on_green'))
                    
                    if destinataires:
                        print(f'FAKE mail to{destinataires}')
                    else:
                        messages.error(request, "Veuillez saisir au moins une adresse email.")
                        
                    main_page = data.get(left_pages)                    
                    if main_page:
                        print(f'FAKE mail to{destinataires} pour {main_page}')
                    else:
                        messages.error(request, "Veuillez sélectionner une page.")
                        
                elif right_pages:
                    print(colored('right_pages', 'cyan'), colored(right_pages, 'white', 'on_cyan'))
                    commissions = data.get('commissions')
                    main_page = data.get(commissions) if commissions else data.get(right_pages)
                    
                    if attachments and hasattr(main_page, 'convocation_documents'):
                        attachments = main_page.convocation_documents.all()
                                            
                    if main_page and hasattr(main_page, 'get_parent'):
                        parent_page = main_page.get_parent().specific if hasattr(main_page.get_parent(), 'specific') else None
                        page_url = main_page.url if hasattr(main_page, 'url') else None
                    elif main_page:
                        messages.error(request, "La page principale n'a pas de parent.")
                    else:
                        messages.error(request, "Aucune page principale n'a été sélectionnée.")

                    print(parent_page)
                    if parent_page and hasattr(parent_page, 'get_members'):
                        members = parent_page.get_members()
                        print(members)
                        for role, users in members.items():
                            for user in users:
                                if hasattr(user, 'email'):
                                    date_fr = formats.date_format(main_page.date, "d F Y")
                                    heure_fr = formats.date_format(main_page.date, "H:i")
                                    sujet = f"Convocation {parent_page.title} du {date_fr}"
                                    contenu = f"Bonjour {user.get_full_name()}, nous avons le plaisir de vous inviter à la réunion de {parent_page.title} qui se tiendra le {date_fr} à {heure_fr}. Vous trouverez ci-joint la convocation et l'ordre du jour. Cordialement, "
                                    # destinataire = [user.email]
                                    destinataires = ['makh@tutanota.com', '09140@tuta.io', 'nic@tuta.com']
                                    destinataire = [random.choice(destinataires)]
                                    email_data.append((sujet, contenu, 'convocation', destinataire))

                    print(colored('Page :', 'red'), colored(main_page, 'white', 'on_red'), colored('Url:', 'red'), colored(page_url, 'white', 'on_red'), colored('Page parent:', 'red'), colored(parent_page, 'white', 'on_red'))
                    print(colored('attachments', 'red'), colored(attachments, 'white', 'on_red'))
                    print(colored('destinataires', 'red'), colored(destinataires, 'white', 'on_red'))
                    print(colored('nombre de membres', 'red'), colored(len(email_data), 'white', 'on_red'))
                    # print(colored('sujets', 'red'), colored(sujets, 'white', 'on_red'))
                    print(colored('DATA', 'red'), colored(email_data, 'white', 'on_green'))     
                    
                    if email_data:
                        email_sender.send_mass_email(email_data)
                        messages.success(request, f"{len(email_data)} mails envoyés avec succès pour la convocation {parent_page.title} du {date_fr}.")
                    else:
                        messages.error(request, "Aucun email n'a été envoyé. Vérifiez les données fournies.")
                else:
                    messages.error(request, "Veuillez sélectionner un type de page à traiter (amicale, bureaux, etc.)")    

            except Exception as e:
                messages.error(request, f"Une erreur s'est produite lors de la tentative d'envoi des emails: {str(e)}")
        else:
            messages.error(request, "Le formulaire n'est pas valide. Veuillez corriger les erreurs.")
    else:
        form = EmailForm()

    return render(request, 'mailing/mailing_form.html', {'pages': pages, 'form': form})