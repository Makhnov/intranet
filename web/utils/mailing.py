from django.core.mail import send_mail, get_connection
from django.conf import settings

def cgs_mail (subject, message, expediteur, destinataires):

    # Créer une connexion avec la configuration spécifique
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        use_tls=settings.EMAIL_USE_TLS,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
    )

    # Utiliser cette connexion pour envoyer l'email
    send_mail(
        subject,
        message,
        f'{expediteur}@cagiregaronnesalat.fr',
        destinataires,
        connection=connection,
    )
    
# Test
# from utils.mailing import cgs_mail
# cgs_mail(
#     'Test',
#     'Message',
#     'instance',
#     ['09140@tuta.io', 'makh@tutanota.com', 'nic@tuta.com'],
# )