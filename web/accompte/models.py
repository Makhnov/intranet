# Page de menu
from utils.menu_pages import MenuPage, menu_page_save

# Traduction
from django.utils.translation import gettext_lazy as _


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