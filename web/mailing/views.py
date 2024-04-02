from termcolor import colored
import random
import mimetypes
from django.contrib.auth.decorators import permission_required
from administration.models import ConvocationPage
from django.shortcuts import render, redirect
from wagtail.admin import messages
from wagtail.models import Page
from mailing.forms import EmailForm
from utils.mailing import EmailSender
from utils.pdf import getPdfFromUrl, generate_pdf
from django.utils import formats, timezone
from django.utils import translation
translation.activate('fr-fr')

@permission_required('mailing.can_send_mail', raise_exception=True)
def mailing_view(request):
    pages = Page.objects.live().specific()
    form = EmailForm(request.POST or None, request.FILES or None, request=request)
    if request.method == 'POST':        
        if form.is_valid():
            try:                
                top_form = form.top_section
                left_form = form.left_section
                right_form = form.right_section
                                
                email_sender = EmailSender(request.user)
                attachments = False
                email_attachments = []
                destinataires = []
                email_data = []

                if 'submit_left' in request.POST:
                    if left_form.is_valid():
                        data = left_form.cleaned_data
                        left_pages = data.get('left_pages')
                        print(colored('left_pages', 'green'), colored(left_pages, 'white', 'on_green'))

                        
                        destinataires = data.get('mail_to')                    
                        if destinataires:
                            print(f'FAKE mail to{destinataires}')
                        else:
                            messages.error(request, "Veuillez saisir au moins une adresse email.")
                            
                        main_page = data.get(left_pages)                    
                        if main_page:
                            print(f'FAKE mail to{destinataires} pour {main_page}')
                        else:
                            messages.error(request, "Veuillez sélectionner une page.")  
                        
                        if main_page and destinataires:
                            # on itere sur tous les destinataires
                            for destinataire in destinataires:                            
                                date_fr = formats.date_format(main_page.date, "d F Y") if hasattr(main_page, 'date') else formats.date_format(timezone.localtime(), "d F Y")  # Modifiez ici                       
                                heure_fr = formats.date_format(main_page.date, "H:i") if hasattr(main_page, 'date') else formats.date_format(timezone.localtime(), "H:i")  # Et ici
                            
                                sujet = f"Invitation {main_page.title} du {date_fr}"
                                contenu = f"Bonjour, nous avons le plaisir de vous inviter à la sortie {main_page.title} qui se tiendra le {date_fr} à {heure_fr}. A très vite, l'Amicale."
                                email_data.append((sujet, contenu, 'convocation', destinataires))                      
                                
                                print(colored('sujet', 'red'), colored(sujet, 'white', 'on_red'))
                                print(colored('contenu', 'red'), colored(contenu, 'white', 'on_red'))
                                print(colored('destinataire', 'red'), colored(destinataire, 'white', 'on_red'))
                                print(colored('email_data', 'red'), colored(email_data, 'white', 'on_red'))
                            
                            if email_data:
                                messages.success(request, f"{len(email_data)} mails envoyés avec succès pour la sortie {main_page.title} du {date_fr}.")
                                return redirect('mailing')
                            else:
                                messages.error(request, "Aucun email n'a été envoyé. Vérifiez les données fournies.")
                        else:
                            messages.error(request, "Veuillez sélectionner une page et saisir au moins une adresse email.")
                    else:
                        messages.error(request, "Le formulaire n'est pas valide. Veuillez corriger les erreurs.")
                elif 'submit_right' in request.POST:
                    if right_form.is_valid():
                        data = right_form.cleaned_data
                        right_pages = data.get('right_pages')
                        print(colored('right_pages', 'cyan'), colored(right_pages, 'white', 'on_cyan'))
                        
                        commissions = data.get('commissions')
                        main_page = data.get(commissions) if commissions else data.get(right_pages)
                        print(colored('commissions', 'cyan'), colored(commissions, 'white', 'on_cyan'))
                        print(colored('main_page', 'cyan'), colored(main_page, 'white', 'on_cyan'))
                        
                        attachments = data.get('right_attachments')
                        if attachments and hasattr(main_page, 'convocation_documents'):
                            attachments = main_page.convocation_documents.all()
                            print(colored('attachments', 'cyan'), colored(attachments, 'white', 'on_cyan'))
                        else:
                            messages.error(request, "Aucune pièce jointe n'a été trouvée pour cette page.")
                        
                        for attachment in attachments:
                            document = attachment.document
                            if document and hasattr(document, 'filename'):
                                attachment_title = document.filename
                            elif document:
                                messages.error(request, "Assurez-vous que le document a un nom de fichier.")
                            else:
                                messages.error(request, "Aucun document n'a été trouvé.")
                                    
                            print(colored('attachment_title', 'cyan'), colored(attachment_title, 'white', 'on_cyan'))
                                
                            if hasattr(document, 'file'):
                                file = document.file
                                if hasattr(file, 'path'):
                                    attachment_path = file.path
                                        
                            print(colored('attachment_path', 'cyan'), colored(attachment_path, 'white', 'on_cyan'))
                                    
                            try:
                                with document.file.open('rb') as file:
                                    email_attachments.append((attachment_title, file.read(), mimetypes.guess_type(attachment_path)[0]))
                            except Exception as e:
                                print(f"Erreur lors de la lecture du fichier {attachment_title}: {e}")

                    
                        if main_page and hasattr(main_page, 'get_parent'):
                            parent_page = main_page.get_parent().specific if hasattr(main_page.get_parent(), 'specific') else None
                            # page_url = main_page.url if hasattr(main_page, 'url') else None
                        elif main_page:
                            messages.error(request, "La page principale n'a pas de parent.")
                        else:
                            messages.error(request, "Aucune page n'a été sélectionnée (Sélectionnez une convocation en fonction de sa date dans le menu déroulant).")
                        
                        if parent_page and hasattr(parent_page, 'get_members'):
                            members = parent_page.get_members()
                            for role, users in members.items():
                                for user in users:
                                    if hasattr(user, 'email'):
                                        date_fr = formats.date_format(main_page.date, "d F Y")
                                        heure_fr = formats.date_format(main_page.date, "H:i")
                                        sujet = f"Convocation {parent_page.title} du {date_fr}"
                                        contenu = f"Bonjour {user.get_full_name()}, nous avons le plaisir de vous inviter à la réunion de {parent_page.title} qui se tiendra le {date_fr} à {heure_fr}. Vous trouverez ci-joint la convocation et l'ordre du jour. Cordialement, "
                                        destinataire = [user.email]
                                        # destinataires = ['makh@tutanota.com', '09140@tuta.io', 'nic@tuta.com']
                                        # destinataire = [random.choice(destinataires)]
                                        email_data.append((sujet, contenu, 'convocation', destinataire))
                                # break
                        else:
                            messages.error(request, "Aucun membre n'a été trouvé pour cette page.")                        

                        if email_data:
                            email_sender.send_mass_email(email_data, attachments=email_attachments)
                            messages.success(request, f"{len(email_data)} mails envoyés avec succès pour la convocation {parent_page.title} du {date_fr}.")
                            return redirect('mailing')
                        else:
                            messages.error(request, "Aucun email n'a été envoyé. Vérifiez les données fournies.")              
                    else:
                        messages.error(request, "Le formulaire n'est pas valide. Veuillez corriger les erreurs.")
                elif 'submit_top' in request.POST:        
                    if top_form.is_valid():
                        data = top_form.cleaned_data
                        ID = data.get('pdf_page')
                        page = ConvocationPage.objects.get(id=ID)
                        print(colored('page', 'yellow'), colored(page, 'white', 'on_yellow'))

                        if page and hasattr(page, 'url'):
                            template_name = 'administration/widgets/template.html'
                            context = {'page': page}
                            css_filenames = ['css/weasyprint.min.css']
                            pdf_filename = f'{page.slug}.pdf'
                            page_url = f'{request.build_absolute_uri(page.url)}'
                            pdf_url = f'{page_url}pdf'
                            print(colored('url', 'yellow'), colored(pdf_url, 'white', 'on_yellow'))
                            # pdf = getPdfFromUrl(request, pdf_url, slug)
                            pdf_path = generate_pdf(request, template_name, context, css_filenames, pdf_filename)
                            print(colored('pdf', 'yellow'), colored(pdf_path, 'white', 'on_yellow'))
                            return redirect('mailing')
                        elif page:
                            messages.error(request, "La page n'a pas d'URL.")
                        else:
                            messages.error(request, "Pour générer un PDF il faut sélectionner une page dans le formulaire de droite.")
                        
                        if pdf_url:
                            print(colored('pdf', 'yellow'), colored(pdf_url, 'white', 'on_yellow'))
                            return redirect('mailing')
                        else:
                            messages.error(request, "Impossible de trouver le PDF.")
                    else:
                        messages.error(request, "Le formulaire n'est pas valide. Veuillez corriger les erreurs.")

            except Exception as e:
                messages.error(request, f"Une erreur s'est produite lors de la tentative d'envoi des emails: {str(e)}")
        else:
            messages.error(request, "Le formulaire n'est pas valide. Veuillez corriger les erreurs.")
    else:
        form = EmailForm()

    return render(request, 'mailing/mailing_form.html', {'pages': pages, 'form': form})

# print(colored('Page :', 'red'), colored(main_page, 'white', 'on_red'), colored('Url:', 'red'), colored(page_url, 'white', 'on_red'), colored('Page parent:', 'red'), colored(parent_page, 'white', 'on_red'))
# print(colored('attachments', 'red'), colored(attachments, 'white', 'on_red'))
# print(colored('destinataires', 'red'), colored(destinataires, 'white', 'on_red'))
# print(colored('nombre de membres', 'red'), colored(len(email_data), 'white', 'on_red'))
# print(colored('DATA', 'red'), colored(email_data, 'white', 'on_green'))