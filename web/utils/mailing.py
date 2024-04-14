from django.core.mail import EmailMessage, send_mail, send_mass_mail, get_connection
from django.core.exceptions import PermissionDenied
from mailing.models import SentMail
from django.conf import settings

# Gestionnaire d'envoi de mail
class EmailSender:
    def __init__(self, user):
        self.user = user

    def can_send_emails(self):
        # Vérifier si l'utilisateur a la permission d'envoyer des emails        
        return self.user.has_perm('mailing.can_send_mail')

    def send_email(self, sujet, contenu, destinataire, expediteur='noreply', fichiers=None):
        if not self.can_send_emails():
            raise PermissionDenied("L'utilisateur n'a pas la permission d'envoyer des emails.")
        
        try:
            cgs_mail(sujet, contenu, expediteur, [destinataire], fichiers)
            # Enregistrement du succès pour chaque destinataire
            SentMail.objects.create(subject=sujet, message=contenu, recipient=destinataire, sent_successfully=True)
        except Exception as e:
            # Enregistrement de l'échec
            SentMail.objects.create(subject=sujet, message=contenu, recipient=destinataire[0], sent_successfully=False, error_message=str(e))
            raise

    def send_mass_email(self, email_data, attachments=None):
        if not self.can_send_emails():
            raise PermissionDenied("L'utilisateur n'a pas la permission d'envoyer des emails.")
        
        try:
            if attachments:
                for email_info in email_data:
                    email_info['fichiers'] = attachments
            
            cgs_mass_mail(email_data)
            # Enregistrement du succès pour chaque email envoyé
            for data in email_data:
                for recipient in data['destinataires']:
                    SentMail.objects.create(subject=data['sujet'], message=data['message'], recipient=recipient, sent_successfully=True)
        except Exception as e:
            # Enregistrement de l'échec pour le premier destinataire comme exemple d'erreur
            SentMail.objects.create(subject=email_data[0]['sujet'], message=email_data[0]['message'], recipient=email_data[0]['destinataires'][0], sent_successfully=False, error_message=str(e))
            raise


# Envoi d'un mail avec les mêmes sujets et messages (plusieurs destinataires possibles).        
def cgs_mail(sujet, contenu, expediteur, destinataires, fichiers=None):
    """
    Envoie un email avec la possibilité d'ajouter des pièces jointes.

    :param sujet: Sujet de l'email
    :param contenu: Contenu de l'email
    :param expediteur: Email de l'expéditeur
    :param destinataires: Liste des destinataires de l'email
    :param fichiers: Un dictionnaire des pièces jointes avec le nom du fichier comme clé et le contenu du fichier comme valeur
    """
    
    # Créer une connexion avec la configuration spécifique
    real_backend="django.core.mail.backends.smtp.EmailBackend"    
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        # backend=real_backend,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        use_tls=settings.EMAIL_USE_TLS,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
    )
    
    # Créer l'objet EmailMessage
    email = EmailMessage(
        subject=sujet,
        body=contenu,
        from_email=f'{expediteur}@cagiregaronnesalat.fr',
        to=destinataires,
        connection=connection
    )
    
    # Ajouter les pièces jointes si présentes
    if fichiers:
        for filename, file_content in fichiers.items():
            email.attach(filename, file_content)
                
    # Envoyer l'email
    email.send()

# Envoi de plusieurs mails où chaque mail a un sujet, un message, un expéditeur et une liste de destinataires.
def cgs_mass_mail(email_data):
    """
    Envoie un ensemble d'e-mails, chaque email pouvant contenir des pièces jointes.

    :param email_data: Une liste de dictionnaires, chaque dictionnaire contenant:
                       'sujet': le sujet de l'email,
                       'message': le contenu de l'email,
                       'expediteur': l'adresse email de l'expéditeur,
                       'destinataires': une liste des destinataires,
                       'fichiers': un dictionnaire optionnel des pièces jointes avec le nom du fichier comme clé et le contenu du fichier comme valeur.
    """

    # Créer une connexion avec la configuration spécifique
    real_backend="django.core.mail.backends.smtp.EmailBackend"    
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        # backend=real_backend,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        use_tls=settings.EMAIL_USE_TLS,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
    )

    # Créer et envoyer chaque email
    for email_info in email_data:
        email = EmailMessage(
            subject=email_info['sujet'],
            body=email_info['message'],
            from_email=f"{email_info['expediteur']}@cagiregaronnesalat.fr",
            to=email_info['destinataires'],
            connection=connection
        )

        # Ajouter les pièces jointes si présentes
        fichiers = email_info.get('fichiers', {})
        for filename, file_content in fichiers.items():
            email.attach(filename, file_content)

        email.send()
