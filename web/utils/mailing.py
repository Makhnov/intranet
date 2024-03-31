from django.core.mail import send_mail, get_connection
from django.conf import settings

def cgs_mail(sujet, contenu, expediteur, destinataires):
    real_backend="django.core.mail.backends.smtp.EmailBackend"
    
    # Créer une connexion avec la configuration spécifique
    connection = get_connection(
        #backend=settings.EMAIL_BACKEND,
        backend=real_backend,
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

# Test
# from utils.mailing import cgs_mail
# cgs_mail(
#     'Test',
#     'Message',
#     'instance',
#     ['to1', 'to2', 'to3'],
# )

from django.core.mail import send_mass_mail, get_connection
from django.conf import settings

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
