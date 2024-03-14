from termcolor import colored

from wagtail import hooks
from collections import defaultdict
from django.db import transaction
from django.shortcuts import get_object_or_404

# Modèles
from administration.models import (
    ConvocationPage,
    CompteRenduPage,
    CommissionPage,
    BureauxIndexPage,
    ConseilsIndexPage,
    ConferencesIndexPage,
    ConvocationUser,
    PresenceStatus,
)

# Filtres
from django.db.models import Q

# Convocations en foreign key (onetoone) des Comptes-rendus
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

# Utilisateurs 
from django.contrib.auth import get_user_model
User = get_user_model()

# Date en français
from datetime import datetime, date
import calendar
import locale

# Slugs
from django.utils.text import slugify

# Blocs
from wagtail.blocks import ListBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock

# Custom Blocs
from utils.imports import HeadingDOCXBlock, ParagraphDOCXBlock, ImageDOCXBlock, TableDOCXBlock

#############
# VARIABLES #
############# 

# variables globales
from utils.variables import STOP_WORDS, ROLE_TRANSLATIONS, ITER_COLORS

# Pages concernées pour la création automatique (titre & slug) des Convocations et des Comptes-Rendus
valid_parent_classes = (
    BureauxIndexPage,
    ConseilsIndexPage,
    CommissionPage,
    ConferencesIndexPage,
)

#############
### HOOKS ###
#############

@hooks.register("before_create_page")
def before_create_page_hook(request, parent_page, page_class):
    # S'active uniquement pour CompteRenduPage
    if page_class == CompteRenduPage:
        set_cr_defaults(request, parent_page, page_class=page_class)

@hooks.register("before_edit_page")
def before_edit_page_hook(request, page):
    # S'active uniquement pour CompteRenduPage
    if isinstance(page.specific, CompteRenduPage):
        set_cr_defaults(request, page.get_parent(), page=page)

@hooks.register("after_create_page")
def after_create_page_handler(request, page):
    after_edit_and_create(request, page)
    after_create_only(request, page)

@hooks.register("after_edit_page")
def after_edit_page_handler(request, page):
    after_edit_and_create(request, page)
    after_edit_only(request, page)

# AFTER (EDIT AND CREATE)
def after_edit_and_create(request, page):
    page_specific_administration = page.specific

    # Pour les ConvocationPage et CompteRenduPage, mettez à jour les titres et les slugs
    if isinstance(page_specific_administration, (ConvocationPage, CompteRenduPage)):
        update_convoc_and_cr_defaults(request, page)
        
    if isinstance(page_specific_administration, CompteRenduPage):
        update_presence_status(request, page)
        import_file(request, page)
        
# AFTER (CREATE ONLY)
def after_create_only(request, page):
    page_specific_administration = page.specific
            
    # Pour les ConvocationPage, créez les utilisateurs associés
    if isinstance(page_specific_administration, ConvocationPage):
        create_convocation_users(request, page)

# AFTER (EDIT ONLY)
def after_edit_only(request, page):
    pass

#############
# FONCTIONS #
#############

# Définition des champs par défaut pour les pages de type CompteRenduPage (before)
def set_cr_defaults(request, parent_page, page=None, page_class=None):
    """
    Ce hook s'exécute avant la création ou l'édition d'une page. Il définit certains champs par défaut
    et effectue des vérifications pour les pages de type CompteRenduPage.
    """
    # Determine la classe de page en fonction de l'opération (création ou édition)
    page_to_check = page if page else page_class
    # print(f"Starting set_defaults for: {page_to_check}")    

    # Copie de la requête
    request.POST = request.POST.copy()

    # S'assurer que la page parent est dans les classes valides
    if not isinstance(parent_page.specific, valid_parent_classes):
        return
    convocation_id = request.POST.get("convocation")

    if not convocation_id:
        return

    try:
        convocation = ConvocationPage.objects.get(id=convocation_id)
    except ConvocationPage.DoesNotExist:
        return

    # Vérifie qu'aucun CompteRenduPage n'est associé à la ConvocationPage sélectionnée, à l'exception de la page actuelle (en cours d'édition)
    if CompteRenduPage.objects.filter(convocation=convocation).exclude(id=getattr(page, 'id', None)).exists():
        messages.error(
            request,
            mark_safe(
                "Il existe déjà un compte rendu pour la convocation que vous avez sélectionnée."
                "<br />&#128161;&#160;&#160;&#160;&#160;"
                "Éditez le compte-rendu existant ou choisissez une autre convocation."
            ),
        )
        return HttpResponseRedirect(request.path)

    # Vérifie que la convocation sélectionnée a le même parent que le compte-rendu en cours de création
    if convocation.get_parent().id != parent_page.id or convocation.get_parent().title != parent_page.title:
        messages.error(
            request,
            mark_safe(
                f"Vous avez sélectionné une convocation liée à <strong>{convocation.get_parent().title}</strong>"
                f" mais vous essayez de créer le compte-rendu pour <strong>{parent_page.title}</strong>."
                "<br />&#128161;&#160;&#160;&#160;&#160;"
                f"Sélectionnez une convocation liée à <strong>{parent_page.title}</strong>"
                f" ou quittez cette page et créez un compte-rendu pour <strong>{convocation.get_parent().title}</strong>."
            ),
        )
        return HttpResponseRedirect(request.path)

    # Définition temporaire de la date pour CompteRenduPage à partir de la convocation associée (pour le hook.after)
    request.POST["date"] = convocation.date.isoformat()        

# Définition des titres et slugs pour les pages de type ConvocationPage et CompteRenduPage
def update_convoc_and_cr_defaults(request, page):
    # print(colored(f"Starting title and slugs status update for: {page}", "green"))

    # Copie de la requête
    request.POST = request.POST.copy()        

    user_date = request.POST.get("date")
    # print(f'Date utilisateur : {user_date}')  # Debug # print
    if user_date:
        try:
            # Formatage de la date pour le titre et le slug
            formatted_date_for_title, formatted_date_for_slug = get_formatted_date(user_date)

            # Le préfixe est toujours basé sur le type spécifique de la page
            prefix = page.specific._meta.verbose_name.capitalize()
            
            # Le suffixe change si le parent est une CommissionPage
            parent_page = page.get_parent().specific
            suffix = parent_page.label if hasattr(parent_page, 'label') and parent_page.label else parent_page.title

            # Construction du nouveau titre et slug
            # print(f'Suffixe : {suffix}')  # Debug # print
            new_title = f"{prefix} {suffix} {formatted_date_for_title}"
            # print(f'Nouveau titre : {new_title}')  # Debug # print
            new_slug = slugify(f"{prefix}-{suffix}-{formatted_date_for_slug}")
            # print(f'Nouveau slug : {new_slug}')  # Debug # print
            
            # Mise à jour du titre, slug et date de la page
            page.title = new_title
            page.slug = new_slug
            page.specific.date = user_date
            page.save()  # Sauvegarde du modèle Wagtail (titre et slug)
            page.specific.save()  # Sauvegarde du modèle CR et Convoc (date)
            page.save_revision().publish()

        except ValueError:
            # Gérer l'erreur si la date n'est pas valide
            pass

# Fonction pour récupérer les utilisateurs en fonction de la page parente
def create_convocation_users(request, page):
    # print(colored(f"Starting convc_users status update for: {page}", "green"))

    parent_page = page.get_parent().specific
    # print(f"Le type de parent_page est: {type(parent_page)}")
    
    function_field_mapping = {
        'ConseilsIndexPage': 'function_council',
        'BureauxIndexPage': 'function_bureau',
        'CommissionPage': 'function_commission',
        'ConferencesIndexPage': 'function_conference',
    }
    function_field = function_field_mapping.get(parent_page.__class__.__name__)
    
    #Filtre de base pour récupérer les utilisateurs associés à la page parent
    users = User.objects.filter(
        ~Q(**{function_field: 'empty'}), # Aucune fonction
        ~Q(**{function_field: ''}),  # ""
        ~Q(**{function_field: None}), # ""
        ~Q(**{function_field: '4'})  # Suppléants exclus       
    )

    # On stocke les remplaçants
    substitutes = User.objects.filter(**{function_field: '4'})
    
    # Si la page parente est une commission, on ajoute un filtre pour l'id de la commission
    if isinstance(parent_page, CommissionPage):
        users = users.filter(commission_id=parent_page.id)
        # print(colored(f"CommissionPage détectée : {parent_page}", "green", "on_white"))
        # print(colored(f'users : {users}', "white", "on_yellow"))
        
    # Créer un dictionnaire pour compter les utilisateurs par fonction
    user_count_by_function = defaultdict(int)
    
    # Première boucle pour compter les utilisateurs par fonction
    for user in users:
        function_value = getattr(user, f"get_{function_field}_display")()
        user_count_by_function[function_value] += 1
    
    # Deuxième boucle pour créer les objets ConvocationUser
    for user in users:
        function_value = getattr(user, f"get_{function_field}_display")()
        function_weight = getattr(user, function_field)
        gender_value = user.get_civility_display()
        
        if user_count_by_function[function_value] > 1:
            gender_key = "Pluriel"
        else:
            gender_key = gender_value

        function_value = ROLE_TRANSLATIONS.get(gender_key, {}).get(function_value, function_value)

        if gender_value == "Neutre":
            gender_value = "Monsieur/Madame"

        identity_value = f"{user.first_name} {user.last_name.upper()}"
        
        municipality_value = user.get_municipality_display()
        
        # On récupère le remplaçant associé à la commune de l'utilisateur
        alternate = substitutes.filter(municipality=user.municipality).first()

        cu = ConvocationUser.objects.create(
            convocation=page,
            user=user,
            parent=parent_page,
            function=function_value,
            function_weight=function_weight,
            gender=gender_value,
            identity=identity_value,
            municipality=municipality_value,
            # "presence" à une valeur PRESENT (1) par défaut (integer)
            # "substitute" à une valeur NULL par défaut (foreign key)
            alternate=alternate, # Suppléant officiel (NULL par défaut)
            
        )
        print(f'CU Créée : {cu}')

# Fonction qui met à jour les statuts de présence des utilisateurs
def update_presence_status(request, page):
    # print(colored(f"Starting presence status update for: {page}", "green"))
    # Vérifiez si la requête est une requête POST
    if request.method == 'POST':
        # Récupérez l'ID de la convocation à partir de la requête POST
        convocation_id = request.POST.get('convocation')
        
        # On récupère toutes les données nécessaires au traitement de la requête
        replaced_user_ids = request.POST.getlist('replaced_users')
        unreplaced_user_ids = request.POST.getlist('unreplaced_users')
        substitute_user_list = request.POST.getlist('substitute_users')
        secretary_id = request.POST.get('secretary')
        
        # Manipulation des données        
        substitute_user_ids = [sub_data.split(',')[2] for sub_data in substitute_user_list if sub_data.split(',')[2].lower() != 'false']
        substitute_count = len(substitute_user_ids)
        absent_user_list = replaced_user_ids + unreplaced_user_ids
        
        # On récupère tous les utilisateurs absents (pas l'ID de la ConvocationUser, l'ID de l'utilisateur)
        absent_user_ids = []
        for sub_data in substitute_user_list:
            parts = sub_data.split(',')
            if parts[0] in absent_user_list:
                absent_user_ids.append(parts[1])
                        
        
        if convocation_id is not None:
            # Récupère l'objet ConvocationPage
            convocation = get_object_or_404(ConvocationPage, id=convocation_id)

            # Récupère l'objet CompteRenduPage associé
            compte_rendu_page = get_object_or_404(CompteRenduPage, convocation=convocation)
            
            # Récupère tous les ConvocationUser associés à la convocation
            convocation_users = ConvocationUser.objects.filter(convocation=convocation)            

            # Récupère tous les ID d'utilisateurs associés à la convocation
            user_ids = [str(user.user.id) for user in convocation_users]
            
            # Récupère tous les ID des utilisateurs présents
            present_titular_ids = [user_id for user_id in user_ids if user_id not in absent_user_ids]   
            # Conversion des listes en ensembles pour supprimer les doublons et fusionner
            present_temp_ids = set(present_titular_ids) | set(substitute_user_ids)
            # Conversion de l'ensemble combiné en liste pour le résultat final
            present_ids = list(present_temp_ids)
            
            # LOGS
            # print(f'Users : {user_ids}')
            # print(f'Replaced : {replaced_user_ids}')
            # print(f'Unreplaced : {unreplaced_user_ids}')
            # print(f'Substitutes full list: {substitute_user_list}')
            # print(f'Substitutes : {substitute_user_ids}')
            # print(f'Substitute count : {substitute_count}')
            # print(f'Absents full list : {absent_user_list}')
            # print(f'Absent members : {absent_user_ids}')
            # print(f'Present members : {present_ids}')
            # print(f'Secretary : {secretary_id}')
            
            # Vérification 1 : un utilisateur ne peut pas être à la fois remplacé et non remplacé
            if set(replaced_user_ids).intersection(unreplaced_user_ids):
                messages.error(
                    request,
                    mark_safe(
                        "A member cannot be both replaced and unreplaced. Please check your selection and try again."
                    )
                )
                return

            # Vérification 2 : un substitut ne peut pas remplacer plus d'un membre
            if len(substitute_user_ids) != len(set(substitute_user_ids)):
                # Il y a des doublons, donc au moins un substitut est utilisé plus d'une fois
                messages.error(
                    request,
                    mark_safe(
                        "A substitute cannot replace more than one member. Please check your selection and try again."
                    )
                )
                return

            # Vérification 3 : il doit y avoir un substitut pour chaque membre remplacé qui a besoin d'un substitut
            if len(replaced_user_ids) != substitute_count:
                messages.error(
                    request,
                    mark_safe(
                        "At least one of your replaced members does not have a substitute. Select one or move the initial member to the 'unreplaced' section. Please check your selection and try again."
                    )
                )
                return
        
            # Vérification 4 : un membre absent ne peut pas être désigné comme suppléant
            if any(sub_id in absent_user_ids for sub_id in substitute_user_ids):
                messages.error(
                    request,
                    mark_safe("You cannot give procuration to an absent member. Please check your selection and try again.")
                )
                return
            

            # Vérification 5 : le secrétaire doit être parmi les membres présents
            if secretary_id and secretary_id not in present_ids:
                messages.error(
                    request,
                    mark_safe("The selected secretary must be present. Please check your selection and try again.")
                )
                return

             
            with transaction.atomic():  # Début d'une transaction pour assurer l'intégrité des données
                
                # Mise à jour des présences
                for convocation_user in convocation_users:
                    user_id_str = str(convocation_user.id)  # Convertir l'ID en chaîne pour la comparaison

                    if user_id_str in replaced_user_ids:
                        convocation_user.presence = PresenceStatus.REPLACED
                        convocation_user.save()
                    elif user_id_str in unreplaced_user_ids:
                        convocation_user.presence = PresenceStatus.UNREPLACED
                        convocation_user.save()
                    else:
                        convocation_user.presence = PresenceStatus.PRESENT
                        convocation_user.save()                       
                  
                # Traitement des utilisateurs substituts
                for data in substitute_user_list:
                    if data:  # vérifier que la donnée n'est pas vide
                        convocation_id, user_id, substitute_value = data.split(',')

                        # Récupérer l'objet ConvocationUser par son ID de convocation
                        convocation_user = convocation_users.get(id=convocation_id)

                        # Mettre à jour le champ substitute_id en fonction de la valeur de substitute_value
                        if substitute_value.lower() == 'false':
                            # Si la valeur est 'false', alors il n'y a pas de substitut
                            convocation_user.substitute_id = None
                        else:
                            # Sinon, utiliser la valeur de l'ID du substitut fournie
                            convocation_user.substitute_id = substitute_value

                        # Sauvegarder l'objet mis à jour
                        convocation_user.save()

                # Sauvegarder les modifications apportées à CompteRenduPage
                compte_rendu_page.save()

        else:
            # print("ID de convocation non fourni")
            pass

# Fonction pour formater la date en français
def get_formatted_date(user_date):
    if isinstance(user_date, str):
        # La chaîne pourrait être une date ou une date-heure, donc on essaie les deux
        try:
            parsed_date = datetime.fromisoformat(user_date).date()  # Convertir en objet date
        except ValueError:
            parsed_date = date.fromisoformat(user_date)  # Si c'est juste une date
    elif isinstance(user_date, datetime):
        parsed_date = user_date.date()  # Extraire la date de datetime
    elif isinstance(user_date, date):
        parsed_date = user_date
    else:
        raise ValueError("Invalid date format")

    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
    formatted_date_for_title = parsed_date.strftime(
        "%d {} %Y".format(calendar.month_name[parsed_date.month].capitalize())
    )
    formatted_date_for_slug = parsed_date.strftime("%d-%m-%Y")
    return formatted_date_for_title, formatted_date_for_slug

# Fonction pour récupérer le préfixe de la page parente
def get_page_prefix(page_type):
    type_map = {ConvocationPage: "convocation", CompteRenduPage: "compte-rendu"}
    return type_map.get(page_type, "")
  
# Fonction pour traiter les fichiers PDF et DOCX
def import_file(request, page):
    page_specific = page.specific
    cr_date = page_specific.date
    collection_restrictions = page.get_view_restrictions()

    if cr_date:
        formatted_date = cr_date.strftime('%d/%m/%Y')
        collection_date = f"CR {formatted_date}"
    else:
        collection_date = "CR Date unknown"
    
    # Initialiser une nouvelle liste pour stocker les blocs mis à jour
    new_blocks = []

    # Itérer sur tous les blocs du StreamField
    for block in page_specific.body:      
                  
        # Le bloc est un type de bloc PDF
        if block.block_type == 'PDF':
            print(colored(f"PDF BLOCK", "white", "on_green"))
            
            # Vérifier si l'utilisateur souhaite importer le PDF
            if block.value.get('pdf_import'):                
                print(colored(f"IMPORTED BLOCK", "yellow"))
                document = block.value.get('pdf_document')
                
                # Vérifier si le document est un fichier PDF
                if document and document.filename.split(".")[-1].lower() == 'pdf':
                    print(colored(f"FILE IS PDF", "green"))                                        
                    
                    # Appeler la méthode pour obtenir les images du PDF et récupérer les IDs des images
                    image_ids = block.block.get_content(document, collection_date, collection_restrictions)

                    # Convertir les IDs en une ListValue pour le bloc
                    images_list_value = ListBlock(ImageChooserBlock()).to_python(image_ids)
                    
                    # On met à jour le champ images du bloc avec la ListValue
                    block.value['pdf_images'] = images_list_value
                    
                    # Ajouter le bloc PDF mis à jour à la liste des nouveaux blocs
                    new_blocks.append((block.block_type, block.value))
                
                else: # Le BLOC est un PDF, l'utilisateur souhaite lancer l'import, MAIS le FICHIER n'est PAS un PDF
                    print(colored(f"FILE IS NOT A PDF : {document.filename}", "magenta", "on_white"))                
                    new_blocks.append((block.block_type, block.value))
            
            else:# Le BLOC est un PDF, MAIS l'utilisateur ne souhaite PAS l'importer
                print(colored(f"NOT IMPORTED BLOCK", "yellow", "on_white"))
                new_blocks.append((block.block_type, block.value))
        
        # Le bloc est un bloc de type DOCX
        elif block.block_type == 'DOCX':
            print(colored(f"DOCX BLOCK", "white", "on_green"))

            # Vérifier si l'utilisateur souhaite importer le DOCX
            if block.value.get('docx_import'):
                print(colored(f"IMPORTED BLOCK", "yellow"))
                document = block.value.get('docx_document')

                # Vérifier si le document est un fichier DOCX
                if document and document.filename.split(".")[-1].lower() == 'docx':
                    print(colored(f"FILE IS DOCX", "green"))
                    
                    # Appeler la méthode pour obtenir le contenu HTML du DOCX et récupérer l'ID de l'image
                    content = block.block.get_content(document, collection_date, collection_restrictions)

                    stream_block = StreamBlock([
                        ('heading', HeadingDOCXBlock()),
                        ('paragraph', ParagraphDOCXBlock()),
                        ('image', ImageDOCXBlock()),
                        ('table', TableDOCXBlock()),                        
                    ])
                    
                    # Créer une liste de dictionnaires pour chaque élément de contenu
                    stream_data = []
                    
                    i = 0
                    bg_colors = ITER_COLORS
                    for element in content:
                        
                        i += 1
                        color_index = (i - 1) % 6
                        # print(colored(f"ELEMENT {i}: {element[0]}", "white", bg_colors[color_index]))
                        
                        if element[0] == 'heading':
                            stream_data.append({
                                'type': 'heading',
                                'value': {
                                    'heading': element[1][1],  
                                    'heading_level': element[1][0],
                                }
                            })
                        elif element[0] == 'paragraph':
                            stream_data.append({
                                'type': 'paragraph',
                                'value': {
                                    'paragraph': element[1],  
                                    # 'position': 'justify',  
                                }
                            })
                        elif element[0] == 'image':                            
                            stream_data.append({
                                'type': 'image',
                                'value': {
                                    'image': element[1],  
                                    # 'size': 'medium',
                                    # 'position': 'center',
                                }
                            })
                        elif element[0] == 'table':
                            stream_data.append({
                                'type': 'table',
                                'value': {
                                    'table': element[1], 
                                    # 'size': 'medium',
                                    # 'position': 'center',
                                }
                            })                   
                                                  
                    # Créer un StreamValue basé sur le StreamBlock et les données dynamiques
                    stream_value = stream_block.to_python(stream_data)

                    # Mettre à jour 'docx_content' avec le nouveau StreamValue
                    block.value['docx_content'] = stream_value

                    # # Ajouter le bloc DOCX mis à jour à la liste du streamfield
                    new_blocks.append((block.block_type, block.value))
                
                else: # Le BLOC est un DOCX, l'utilisateur souhaite lancer l'import, MAIS le FICHIER n'est PAS un DOCX
                    print(colored(f"FILE IS NOT A DOCX : {document.filename}", "magenta", "on_white"))
                    new_blocks.append((block.block_type, block.value))
                
            else:# Le BLOC est un DOCX, l'utilisateur ne souhaite PAS l'importer
                print(colored(f"NOT IMPORTED BLOCK", "yellow", "on_white"))
                new_blocks.append((block.block_type, block.value))
                
        # Le bloc est un bloc de type CHART
        elif block.block_type == 'chart':
            print(colored(f"CHART BLOCK", "white", "on_green"))
            # print(colored(f"BLOCK VALUE: {block.value[0]}", "white", "on_green"))
            
            from bs4 import BeautifulSoup
            import json

            # Votre chaîne HTML du bloc 'chart', obtenue de block.value
            html_content = str(block.value)

            # Analyser le HTML avec BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Trouver l'élément canvas et extraire l'attribut 'data-datasets'
            canvas = soup.find('canvas')
            data_datasets = canvas['data-datasets'] if canvas else '{}'

            # Assurez-vous que data_datasets est une chaîne avant de l'analyser avec json.loads()
            if isinstance(data_datasets, str):
                data_json = json.loads(data_datasets)
                print("DATAJSON", data_json)
            else:
                # Si data_datasets est déjà un dictionnaire (ou tout objet non chaîne), pas besoin de json.loads()
                print("DATASET", data_datasets)

                
                # # Vérifier si l'utilisateur souhaite importer le CHART
                # if block.value.get('chart_import'):
                #     print(colored(f"IMPORTED BLOCK", "yellow"))
                #     document = block.value.get('chart_document')

                # # Appeler la méthode pour obtenir le contenu HTML du CHART et récupérer l'ID de l'image
                # content = block.block.get_content(document, collection_date, collection_restrictions)

                # # Mettre à jour 'chart_content' avec le contenu HTML
                # block.value['chart_content'] = content
                # print(colored(f"CONTENT: {content}", "white", "on_green"))
                
                # # Ajouter le bloc CHART mis à jour à la liste du streamfield
            new_blocks.append((block.block_type, block.value))
            
        else:# Le BLOC n'est ni un PDF ni un DOCX
            print(colored(f"NOT PDF BLOCK", "red", "on_white"))
            new_blocks.append((block.block_type, block.value))
            
    # Mise à jour du StreamField avec les blocs mis à jour
    page_specific.body = new_blocks
    # page_specific.save()
    page_specific.save_revision().publish()