import os
from django.core.mail import send_mail, get_connection
from django.conf import settings

def cgs_mail (subject, message, recipient_list, email_type):
    email_settings = {
        'contact': {
            'EMAIL_HOST_USER': os.getenv("CONTACT_EMAIL", "contact@cagiregaronnesalat.fr"),
            'EMAIL_HOST_PASSWORD': os.getenv("CONTACT_EMAIL_PASSWORD", "pass"),
        },
        'administration': {
            'EMAIL_HOST_USER': os.getenv("ADMINISTRATION_EMAIL", "convocation@cagiregaronnesalat.fr"),
            'EMAIL_HOST_PASSWORD': os.getenv("ADMINISTRATION_EMAIL_PASSWORD", "pass"),
        },                                         
        'amicale': {
            'EMAIL_HOST_USER': os.getenv("AMICALE_EMAIL", "amicale@cagiregaronnesalat.fr"),
            'EMAIL_HOST_PASSWORD': os.getenv("AMICALE_EMAIL_PASSWORD", "pass"),
        },
    }

    # Sélectionner la configuration basée sur email_type
    config = email_settings.get(email_type)

    # Créer une connexion avec la configuration spécifique
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        use_tls=settings.EMAIL_USE_TLS,
        username=config['EMAIL_HOST_USER'],
        password=config['EMAIL_HOST_PASSWORD'],
    )

    # Utiliser cette connexion pour envoyer l'email
    send_mail(
        subject,
        message,
        config['EMAIL_HOST_USER'],  # from_email, ici on utilise le username spécifique au contexte
        recipient_list,
        connection=connection,  # Passer la connexion personnalisée ici
    )

# Test
# cgs_mail(
#     'Test',
#     '<3',
#     ['clemence.vezin@cagiregaronnesalat.fr'],
#     'contact'  
# )