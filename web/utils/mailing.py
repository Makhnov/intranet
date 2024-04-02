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

    def send_email(self, sujet, contenu, destinataire, expediteur='noreply'):
        if not self.can_send_emails():
            raise PermissionDenied("L'utilisateur n'a pas la permission d'envoyer des emails.")
        
        try:
            cgs_mail(sujet, contenu, expediteur, destinataire)
            # Enregistrement du succès pour chaque destinataire
            SentMail.objects.create(subject=sujet, message=contenu, recipient=destinataire, sent_successfully=True)
        except Exception as e:
            # Enregistrement de l'échec
            SentMail.objects.create(subject=sujet, message=contenu, recipient=destinataire, sent_successfully=False, error_message=str(e))
            raise

    def send_mass_email(self, email_data, attachments=None):
        if not self.can_send_emails():
            raise PermissionDenied("L'utilisateur n'a pas la permission d'envoyer des emails.")
        
        try:
            for sujet, contenu, expediteur, destinataires in email_data:
                email = EmailMessage(
                    subject=sujet,
                    body=contenu,
                    from_email=f'{expediteur}@cagiregaronnesalat.fr',
                    to=destinataires,
                    connection=get_connection(
                        backend=settings.EMAIL_BACKEND,
                        host=settings.EMAIL_HOST,
                        port=settings.EMAIL_PORT,
                        use_tls=settings.EMAIL_USE_TLS,
                        username=settings.EMAIL_HOST_USER,
                        password=settings.EMAIL_HOST_PASSWORD,
                    )
                )
                # Attacher les pièces jointes
                if attachments:
                    for attachment in attachments:
                        email.attach(attachment[0], attachment[1], attachment[2])
                
                email.send()

                # Enregistrement du succès pour chaque destinataire
                for recipient in destinataires:
                    SentMail.objects.create(subject=sujet, message=contenu, recipient=recipient, sent_successfully=True)
        
        except Exception as e:
            # Enregistrement de l'échec
            SentMail.objects.create(subject=sujet, message=contenu, recipient=destinataires[0], sent_successfully=False, error_message=str(e))
            raise
        
# Envoi d'un mail avec les mêmes sujets et messages (plusieurs destinataires possibles).        
def cgs_mail(sujet, contenu, expediteur, destinataires):
    real_backend="django.core.mail.backends.smtp.EmailBackend"
    
    # Créer une connexion avec la configuration spécifique
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        # backend=real_backend,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        use_tls=settings.EMAIL_USE_TLS,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
    )
    
    # Utiliser cette connexion pour envoyer l'email
    send_mail(
        sujet,
        contenu,
        f'{expediteur}@cagiregaronnesalat.fr',
        [destinataires],
        connection=connection,
    )

# Envoi de plusieurs mails où chaque mail a un sujet, un message, un expéditeur et une liste de destinataires.
def cgs_mass_mail(email_data):
    """
    Envoie un ensemble d'e-mails en utilisant la fonction send_mass_mail de Django.

    :param email_data: Une liste de tuples, chaque tuple contenant:
                       (sujet, message, expéditeur, liste_destinataires)
    """
    # Créer une connexion avec la configuration spécifique
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        use_tls=settings.EMAIL_USE_TLS,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
    )

    # Préparer les données d'email pour send_mass_mail
    prepared_emails = []
    for sujet, contenu, expediteur, destinataires in email_data:
        email_tuple = (sujet, contenu, f'{expediteur}@cagiregaronnesalat.fr', destinataires)
        prepared_emails.append(email_tuple)

    # Utiliser send_mass_mail pour envoyer les e-mails
    send_mass_mail(tuple(prepared_emails), connection=connection)
