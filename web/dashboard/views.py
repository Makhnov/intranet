from termcolor import colored
import random

from django.shortcuts import render
from wagtail.admin import messages
from wagtail.models import Page
from dashboard.forms import EmailForm
from utils.mailing import cgs_mail, cgs_mass_mail
from django.utils import formats
from django.utils import translation
translation.activate('fr-fr')

def mailing_view(request):
    pages = Page.objects.live().specific()
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            attachments = False
            destinataires = []
            main_page = ''
            
            data = form.cleaned_data
            left_pages = data.get('left_pages')
            right_pages = data.get('right_pages')        

            # si left_pages on récupère le type de page
            if left_pages:
                print(colored('left_pages', 'green'), colored(left_pages, 'white', 'on_green'))
                destinataires = form.cleaned_data.get('mail_to')
                attachments = data.get('left_attachments')                
                main_page = data.get(left_pages)
                    
            elif right_pages:
                print(colored('right_pages', 'cyan'), colored(right_pages, 'white', 'on_cyan'))
                commissions = data.get('commissions')
                attachments = data.get('right_attachments')                
                if commissions:
                    main_page = data.get(commissions)
                else:
                    main_page = data.get(right_pages)

            if main_page:
                parent_page = main_page.get_parent().specific if hasattr(main_page.get_parent(), 'specific') else None
                page_url = main_page.url if hasattr(main_page, 'url') else None
                
                if right_pages:
                    print(f"Parent Page Type: {type(parent_page)}")
                    members = parent_page.get_members() if hasattr(parent_page, 'get_members') else None
                
            if attachments:
                attachments = main_page.convocation_documents.all() if hasattr(main_page, 'convocation_documents') else None           
            
            email_data = []
            
            if members:
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
                            
                            # Ajouter le tuple au lot d'emails
                            email_data.append((sujet, contenu, 'convocation', destinataire))

                            
            # Envoi des emails personnalisés en une opération
            try:
                cgs_mass_mail(email_data)
                messages.success(request, "L'email a été envoyé avec succès.")
            except Exception as e:
                print(colored('Exception:', 'red'), colored(str(e), 'white', 'on_red'))
                messages.error(request, "Une erreur s'est produite lors de l'envoi de l'email.")

                            
            # print(colored('Page :', 'red'), colored(main_page, 'white', 'on_red'), colored('Url:', 'red'), colored(page_url, 'white', 'on_red'), colored('Page parent:', 'red'), colored(parent_page, 'white', 'on_red'))
            # print(colored('attachments', 'red'), colored(attachments, 'white', 'on_red'))
            # print(colored('destinataires', 'red'), colored(destinataires, 'white', 'on_red'))
            # print(colored('sujets', 'red'), colored(sujets, 'white', 'on_red'))
            print(colored('DATA', 'red'), colored(email_data, 'white', 'on_green'))                     
    else:
        form = EmailForm()
    return render(request, 'mailing/mailing_form.html', {'pages': pages, 'form': form})

# {
#     'left_pages': '', 
#     'amicale': None, 
#     'ressources': None, 
#     'public': None, 
#     'mail_to': '', 
#     'left_attachments': False, 
#     'right_pages': 'commissions', 
#     'commissions': 'commission_84', 
#     'conseils': None, 
#     'bureaux': None, 
#     'conferences': None, 
#     'commission_84': <ConvocationPage: Convocation af 15 Mars 2024>, 
#     'commission_87': None, 
#     'commission_88': None, 
#     'commission_89': None, 
#     'commission_90': None, 
#     'commission_91': None, 
#     'commission_92': None, 
#     'commission_93': None, 
#     'commission_94': None, 
#     'commission_95': None, 
#     'commission_160': None, 
#     'right_attachments': True
# }
            