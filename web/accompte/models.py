# Utilitaires
from utils.menu_pages import MenuPage, menu_page_save
from utils.variables import THEMES, COLORS

# Traduction
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

####################
##   PROFIL CGS   ##
#################### 

class CGSUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cgs_userprofile')
    theme = models.CharField(max_length=10, choices=[(theme['code'], theme['name']) for theme in THEMES], default='clair')
    icons = models.CharField(max_length=10, choices=[(color['code'], color['name']) for color in COLORS], default='cyan')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

####################
## PAGES DIVERSES ##
#################### 

# Section pages diverses
class AccountPage(MenuPage):
    parent_page_types = ['home.HomePage']
    subpage_types = [
        'accompte.ProfilePage', 
        'accompte.LoginPage', 
        'accompte.LogoutPage', 
        'accompte.SignupPage', 
        'accompte.PasswordPage', 
        'accompte.EmailPage'
    ]
    save = menu_page_save('accompte')
    
# # Page de profil (Menu utilisateur)
class ProfilePage(MenuPage):
    parent_page_types = ['accompte.AccountPage']
    subpage_types = []
    save = menu_page_save('profil')

# Page de connexion (Menu utilisateur)
class LoginPage(MenuPage):
    parent_page_types = ['accompte.AccountPage']
    subpage_types = []    
    save = menu_page_save('connexion')

# Page de déconnexion (Menu utilisateur)
class LogoutPage(MenuPage):
    parent_page_types = ['accompte.AccountPage']
    subpage_types = []
    save = menu_page_save('deconnexion')

# Page d'inscription (Menu utilisateur)
class SignupPage(MenuPage):
    parent_page_types = ['accompte.AccountPage']
    subpage_types = []
    save = menu_page_save('inscription')

# Page de gestion de l'adresse email (Menu utilisateur)
class EmailPage(MenuPage):
    parent_page_types = ['accompte.AccountPage']
    subpage_types = []
    save = menu_page_save('mel')
    
# Page de réinitialisation du mot de passe (Menu utilisateur)
class PasswordPage(MenuPage):
    parent_page_types = ['accompte.AccountPage']
    subpage_types = ["accompte.PasswordResetPage", "accompte.PasswordSetPage", "accompte.PasswordChangePage"]
    save = menu_page_save('mdp')

# Page de réinitialisation du mot de passe (Menu utilisateur)
class PasswordResetPage(MenuPage):
    parent_page_types = ['accompte.PasswordPage']
    subpage_types = []
    save = menu_page_save('mdp_recup')

# Page de modification du mot de passe (Menu utilisateur)
class PasswordChangePage(MenuPage):
    parent_page_types = ['accompte.PasswordPage']
    subpage_types = []
    save = menu_page_save('mdp_modif')

# Page de définition du mot de passe (Menu utilisateur)
class PasswordSetPage(MenuPage):
    parent_page_types = ['accompte.PasswordPage']
    subpage_types = []
    save = menu_page_save('mdp_init')