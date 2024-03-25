from wagtail.models import PageViewRestriction
from termcolor import colored

from accompte.models import (
    AccountPage, 
    ProfilePage, 
    LoginPage,    
    LogoutPage, 
    SignupPage,
    EmailPage, 
    PasswordPage, 
    PasswordResetPage, 
    PasswordChangePage, 
    PasswordSetPage
)
from administration.models import CommissionsIndexPage
from amicale.models import AmicaleIndexPage
from home.models import RessourcesPage, HomePage, PublicPage

# Pages publiques
no_restricted_pages = [
    HomePage, 
    PublicPage, 
    LoginPage, 
    SignupPage,
]

# Pages restreintes aux utilisateurs authentifiés
login_restricted_pages = [
    AmicaleIndexPage,
    RessourcesPage,
    AccountPage, 
    ProfilePage, 
    LogoutPage, 
    EmailPage,
    PasswordPage, 
    PasswordResetPage, 
    PasswordChangePage, 
    PasswordSetPage,
]


# Vérification des droits d'accès aux pages
def check_page_access(user, page, bool):
    # print(colored(f'Checking access for {user} to page {page}', 'black', 'on_white'))
    if user.is_superuser and user.is_active:
        # print(colored(f'Access granted: {user} is a superuser and active', 'black', 'on_green'))
        return True
    if isinstance(page, tuple(no_restricted_pages)):
        # print(colored(f'Access granted: {page} is a public page', 'black', 'on_green'))
        return True
    
    if isinstance(page.specific, CommissionsIndexPage):
        return check_child_pages_access(user, page, True)
    
    # Si bool & pas de restriciton, ou si pas de restriction et pas d'enfants
    if bool and not page.get_view_restrictions().exists() or not page.get_view_restrictions().exists() and not page.get_children().live():
        # print(colored(f'Access granted: {page} has no restrictions and is public by default', 'black', 'on_green'))
        return True   
     
    for restriction in page.get_view_restrictions():
        if restriction.restriction_type == PageViewRestriction.LOGIN:
            if not user.is_authenticated:
                # print(colored(f'Access denied: {user} is not authenticated for page {page}', 'black', 'on_red'))
                return False
            else: 
                # print(colored(f'Access granted: {user} is authenticated for page {page}', 'black', 'on_green'))
                return True
        elif restriction.restriction_type == PageViewRestriction.GROUPS:
            if not any(group in user.groups.all() for group in restriction.groups.all()):
                # print(colored(f'Access denied: {user} does not belong to required groups for page {page}', 'black', 'on_red'))
                return False
            else:
                # print(colored(f'Access granted: {user} belongs to required groups for page {page}', 'black', 'on_green'))
                return True

    return check_child_pages_access(user, page, True)

# Vérification des droits d'accès aux pages enfants
def check_child_pages_access(user, page, bool):
    children = page.get_children().live()

    for child in children:
        if check_page_access(user, child, bool):
            # print(colored(f'Access granted: {user} has access to at least one child of {page} ({child})', 'black', 'on_green'))
            return True
        
    # print(colored(f'Access denied: {user} does not have access to any of the {page} childs', 'black', 'on_red'))
    return False