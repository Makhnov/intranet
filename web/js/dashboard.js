document.addEventListener('DOMContentLoaded', function() {
    whereAmI();
});

// Fonction de routage lors du chargement d'une page
function whereAmI() {
    const bodyClass = document.body ? document.body.getAttribute('class') : '';
    const TITRE = document.title;
    console.log(TITRE);
    console.log(bodyClass);

    // Page d'accueil du Dashboard
    if (bodyClass.includes("homepage")) {
        console.log("Page d'accueil du Dashboard détectée");
        accueil();
    }

    // Pages de l'Amicale (création et édition)
    if (TITRE.includes('Amicale page')) {
        console.log("Page de l'amicale détectée");
        amicale();
    }

    // Page intermédiaire de la création de Convocs ou de CR en passant par Quickcreate (page d'accueil)
    if (document.querySelector('body.ready ul.listing.cgs-quick')) {
        console.log("Page quickcreate détectée");
        quickcreate();
    }

    // Page des FAQ (listes de toutes les questions)
    if (TITRE.includes('Exploring: Agents (FAQ)')) {
        console.log("Liste de la FAQ détectée");
        faqList();
    }

    // Page de listing des utilisateurs
    if (document.querySelector("#listing-results.users")) {
        console.log("Page d'affichage des utilisateurs détectée");
        usersList();
    }

    // Page de création/édition d'utilisateur
    if (document.querySelector("form[action^='/admin/users/'][method='post']")) {
        console.log("Création/édition d'utilisateur détectée");
        userCommissionUpdate();
        userElectedUpdate(); 
    }

    // Page de création/édition d'un évènemenet joyous
    if (document.querySelector("form[action*='joyous/simpleeventpage/'][method='post']")) {
        console.log("Création/édition d'évènement détectée");
        joyousSingleEvent();
    }

    // Page de convocation
    if (TITRE.includes('Convocation')) {
        console.log("Page de convocation détectée");
        convocationDate();
    }

    // Page de Compte-rendu (Récupération des users de la convocation et import de documents type PDF ou DOCX)
    if (TITRE.includes('Compte-rendu')) {
        console.log("Page de compte-rendu détectée");
        compteRenduUsers();
        compteRenduImportBloc();
    }

    // Page de FAQ
    if (TITRE.includes('Faq page')) {
        console.log("Page de FAQ détectée");
        faqPage();
    }
}

////////////////////////////////////////// FONCTIONS GLOBALES //////////////////////////////////////////////////

// Contenu visible/caché
function collapsible(element) {
    // On toggle collapsed sur le parent le plus proche qui possed la classe "cgs-collapsible"
    const collapsible = element.closest('.cgs-collapsible');
    collapsible.classList.toggle('cgs-collapsed');
}

// Mise à jour de l'input pour la liste des fonctions relative aux commissions lors de la création/édition d'utilisateur
function userFunctionUpdate() {
    console.log("Mise à jour de l'input pour la liste des fonctions relative aux commissions");

    const inputs = document.querySelectorAll('input[name="commissions"]:checked');
    const functionsData = [];

    inputs.forEach((input) => {
        // On récupère le select dont la value est égale à celle de l'input
        const select = document.querySelector(`select[data-id="${input.value}"]`);

        if (select) {
            functionsData.push({ "commission": input.value, "function": select.value });
        }
    });

    // Met à jour la valeur de l'input caché avec le JSON des données
    document.getElementById('id_functions_commissions').value = JSON.stringify(functionsData);
}   

// Fonction qui crée un bloc info (look warning pour les ancienne convocations)
function createInfoBlock(id, message) {
    const block = document.getElementById(id);
    if (block) {
        return;
    } else { 
        const div = document.createElement('div');
        div.classList.add('cgs-warning');        
        div.setAttribute('id', id);
        const p = document.createElement('p');
        p.classList.add('warning-message');
        p.textContent = message;
        div.appendChild(p);
        return div;
    }
}

// Fonction qui supprime un bloc info
function removeInfoBlock(id) {
    const block = document.getElementById(id);
    if (block) {
        block.remove();
    }
}

//////////////////////////////////////////    PAGES CHARGEES  //////////////////////////////////////////////////

// Page d'accueil du Dashboard
function accueil() {
    // Sélectionne tous les SVG avec la classe "icon icon" et itère sur chacun
    document.querySelectorAll(".w-summary__list svg.icon").forEach(function(svg) {
        let a = svg.nextElementSibling;  // le lien <a> suivant le SVG
        let url = a.getAttribute("href");  // l'URL du lien <a>

        // Attache un écouteur d'événement "click" au SVG
        svg.addEventListener("click", function() {
            window.location.href = url;  // navigue vers l'URL du lien <a>
        });
    });
}

// Pages de l'Amicale (création et édition)
function amicale() {
    const mapBox = document.querySelector('#id_use_map');
    const idblocks = ["map_details", "details_de_la_carte", "detalles_del_mapa"];
    let mapPanel, idtest;

    for (let id of idblocks) {
        idtest = `panel-child-contenu-${id}-content`;
        mapPanel = document.querySelector(`#${idtest}`);

        if (mapPanel) {
            break;
        }
    }

    const mapBtn = document.querySelector(`.w-panel__toggle[aria-controls="${idtest}"]`);

    function toggleMapPanel() {
        if (mapBox.checked) {
            mapBtn.setAttribute('aria-expanded', 'true');
            mapPanel.classList.remove('disabled');
            mapPanel.querySelectorAll('input, select, textarea').forEach(el => el.disabled = false);
            mapPanel.removeAttribute('hidden');
        } else {
            mapBtn.setAttribute('aria-expanded', 'false');
            mapPanel.classList.add('disabled');
            mapPanel.querySelectorAll('input, select, textarea').forEach(el => el.disabled = true);
            mapPanel.setAttribute('hidden', '');
        }
    }

    toggleMapPanel();
    mapBox.addEventListener('change', toggleMapPanel);
}

// Page intermédiaire de la création de Convocs ou de CR en passant par Quickcreate (page d'accueil)
function quickcreate() {
    const container = document.querySelector('body.ready ul.listing')    
    const items = document.querySelectorAll('body.ready ul.listing li');
    // const H1 = document.querySelector('header h1');
    // const title = H1 ? H1.textContent.split("Création d'")[1] || "" : "";    

    const LI = document.createElement('li');
    LI.classList.add('list', 'cgs-closed');
    LI.setAttribute('data-name', 'Commissions et groupes de travail');
    LI.setAttribute('data-model', 'CommissionPage');
    
    const A = document.createElement('a');
    A.classList.add('icon', 'icon-plus-inverse', 'icon-larger');
    A.setAttribute('ID', 'commissions-dropdown');
    A.setAttribute('alt', 'Ouvrir le menu déroulant des commissions ou groupes de travail');
    A.setAttribute('title', 'Afficher toutes les commissions et groupes de travail');

    const text = document.createElement('strong');
    text.textContent = "Commissions et groupes de travail";
    const icon = document.createElement('span');
    icon.textContent ="▶️"
    //⤵️⤴️🔼🔽▶️◀️

    const UL = document.createElement('ul');
    UL.classList.add('com-listing', 'cgs-quick', 'cgs-hidden');
    
    A.appendChild(text); 
    A.appendChild(icon); 
    LI.appendChild(A);
    LI.appendChild(UL);
    container.appendChild(LI);

    A.addEventListener('click', function() {
        UL.classList.toggle('cgs-hidden');
        LI.classList.toggle('cgs-closed');
        if (UL.classList.contains('cgs-hidden')) {
            icon.textContent = "▶️";
            A.setAttribute('title', 'Afficher toutes les commissions et groupes de travail');
            A.setAttribute('alt', 'Ouvrir le menu déroulant des commissions ou groupes de travail');
        } else {
            icon.textContent = "🔽";
            A.setAttribute('title', 'Masquer toutes les commissions et groupes de travail');
            A.setAttribute('alt', 'Fermer le menu déroulant des commissions ou groupes de travail');
        }
    });

    items.forEach(item => {
        const model = item.getAttribute('data-model');
        if (model === 'CommissionPage') {
            const clone = item.cloneNode(true);
            UL.appendChild(clone);
            item.remove()
        }
    });
}

// Page des FAQ (listes de toutes les questions)
function faqList() {
    // On boucle sur les <a> du thead pour modifier le titre
    const As = document.querySelectorAll("thead th a");
    As.forEach(a => {        
        if (a.title.includes("Titre")) {
            a.textContent = `${a.textContent}: [Thématique] - [Cibles] - [Mots-clef]`;
        }
    });
}

// Page de listing des utilisateurs
function usersList() {
    // Sélectionne l'élément qui va accueillir la liste de choix (partie gauche du header)
    const anchor = document.querySelector('header .left');

    // Création et ajout de l'élément <select> à l'élément <header>
    const select = document.createElement('select');
    select.id = 'pagination-select';

    const options = [
        { value: '20', text: '20' },
        { value: '50', text: '50' },
        { value: '100', text: '100' },
        { value: '10000', text: 'Tous' }
    ];

    const currentPaginateBy = new URLSearchParams(window.location.search).get('paginate_by') || '20';

    options.forEach(option => {
        const optElement = document.createElement('option');
        optElement.value = option.value;
        optElement.textContent = option.text;

        // Définir l'option en cours comme sélectionnée
        if (option.value === currentPaginateBy) {
            optElement.selected = true;
            optElement.setAttribute('selected', 'selected');
        }

        select.appendChild(optElement);
    });

    anchor.appendChild(select);

    select.addEventListener('change', function() {
        const selectedValue = this.value;
        let newUrl;

        if (selectedValue === 'all') {
            newUrl = PaginationURL(window.location.href, 'paginate_by', '');
        } else {
            newUrl = PaginationURL(window.location.href, 'paginate_by', selectedValue);
        }

        window.location.href = newUrl;
    });

    function PaginationURL(url, param, paramVal) {
        let newAdditionalURL = '';
        const tempArray = url.split('?');
        const baseURL = tempArray[0];
        let additionalURL = tempArray[1];
        let temp = '';
    
        if (additionalURL) {
            const tempArray = additionalURL.split('&');
            for (let i = 0; i < tempArray.length; i++) {
                if (tempArray[i].split('=')[0] != param) {
                    newAdditionalURL += temp + tempArray[i];
                    temp = '&';
                }
            }
        }
    
        const rowsTxt = temp + '' + param + '=' + paramVal;
        return baseURL + '?' + newAdditionalURL + rowsTxt;
    }
}

// Page de FAQ 
function faqPage() {

    // Sélectionner le conteneur principal et appliquer le processus
    const answerSection = document.getElementById('panel-child-contenu-answer-section');
    if (answerSection) {
        processButtonBlocks(answerSection);
    } else {
        console.warn('Container #panel-child-contenu-answer-section not found');
    }

    // Fonction pour appliquer les modifications sur les buttonBlock
    function reworkingButtonBlock(element) {
        const URLBlock = element.querySelector('[data-contentpath="url"]');        
        const textBlock = element.querySelector('[data-contentpath="text"]');
        const positionBlock = element.querySelector('[data-contentpath="position"]');
        const colorBlock = element.querySelector('[data-contentpath="color"]');
        const iconBlock = element.querySelector('[data-contentpath="icon"]');

        URLBlock.classList.add('cgs-column6');        
        textBlock.classList.add('cgs-column6');
        positionBlock.classList.add('cgs-column4');
        iconBlock.classList.add('cgs-column4');
        colorBlock.classList.add('cgs-column4');
        element.classList.add('cgs-colbox');       
    }


    function processButtonBlocks(container) {
        // Traiter immédiatement tous les buttonBlock existants
        container.querySelectorAll('.button-block').forEach(reworkingButtonBlock);

        // Utiliser MutationObserver pour écouter les nouveaux buttonBlock
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // ELEMENT_NODE
                        if (node.matches('.button-block')) {
                            reworkingButtonBlock(node);
                        }
                        node.querySelectorAll('.button-block').forEach(reworkingButtonBlock);
                    }
                });
            });
        });

        observer.observe(container, {
            childList: true,
            subtree: true
        });
    }
}

// Page de création/édition d'utilisateur, mise en forme de la section des commissions
function userCommissionUpdate() {    
    // On récupère la liste des options que l'on trie par ordre alphabétique on créee une nouvelle liste avec la même id
    const commissions = document.getElementById('id_commissions');
    const fonctions = document.getElementById('id_functions_commissions');
    const FVALUES =JSON.parse(fonctions.value);
    const tableau = Array.from(commissions.options).sort((a, b) => a.textContent.localeCompare(b.textContent));
    const newCommissions = document.createElement('div');
    newCommissions.setAttribute('id', 'id_commissions');
    const newFonctions = document.createElement('div');
    newFonctions.setAttribute('id', 'id_functions_commissions_list');

    // On récupère tous les Cwrappers
    const CdataField = commissions.parentElement; // Le parent direct de la liste auquel on ajoute la nouvelle liste
    const CmodelField = CdataField.parentElement; // Le grand-parent de la liste dont on modifie les classes
    const Cwrapper = CmodelField.parentElement; // l'arriere grand-parent de la liste dont on supprime le label
    const FdataField = fonctions.parentElement;
    const FmodelField = FdataField.parentElement;
    const Fwrapper = FmodelField.parentElement;
    // Gestion des blocs d'erreurs
    const Ccontent = document.getElementById('commissions-content');    
    // on récupère les <div class="w-field__errors" data-field-errors=""> qui contiennent des enfants
    const Cerrors = Ccontent.querySelectorAll('.w-field__errors[data-field-errors]');
    for (const err of Cerrors) {
        if (err.children.length > 0) {
            console.log("ERREUR TROUVEE");
            Ccontent.insertBefore(err, Ccontent.firstChild);
        }
    }

    tableau.forEach((option, i) => {
        const { function: FONCTION } = FVALUES.find(({ commission }) => commission === option.value) || {};    
        // On remplace l'option par une div/label/input
        const CDIV = document.createElement('div');
        const FDIV = document.createElement('div');
        const CLABEL = document.createElement('label');
        const FSELECT = function_selector(option.textContent, option.value, FONCTION);
        const CINPUT = document.createElement('input');

        // On itere le label dans l'ordre des options
        CLABEL.setAttribute('for', `id_commissions_${i}`);

        // On donne à l'input l'id équivalente au for. Si option selected => input checked
        CINPUT.setAttribute('id', `id_commissions_${i}`);
        CINPUT.setAttribute('type', 'checkbox');
        CINPUT.setAttribute('name', 'commissions');        
        CINPUT.setAttribute('value', option.value);
        if (option.selected) {
            CINPUT.setAttribute('checked', 'checked');
        }

        // Ecouteur d'évenement sur l'input
        CINPUT.addEventListener('change', function() {
            // Sélection du select correspondant via data-id
            const select = document.querySelector(`select[data-id="${this.value}"]`);    
            // Si l'input est coché, ajoute la classe 'cgs-checked', sinon la retire
            if (this.checked) {
                select.classList.add('cgs-checked');
                if (select.value === "") {
                    select.value = "3";
                }
            } else {
                select.classList.remove('cgs-checked');  
                select.value = "";              
            }
        });

        // On ajoute l'input au label, le label à la div et la div à la nouvelle liste
        CLABEL.appendChild(CINPUT);
        CLABEL.appendChild(document.createTextNode(option.textContent));
        CDIV.appendChild(CLABEL);
        FDIV.appendChild(FSELECT);

        newCommissions.appendChild(CDIV);
        newCommissions.addEventListener('change', userFunctionUpdate);
        newFonctions.appendChild(FDIV);
        newFonctions.addEventListener('change', userFunctionUpdate);
    });

    // On remplace la liste dans le parent direct
    CdataField.replaceChild(newCommissions, commissions);
    FdataField.replaceChild(newFonctions, fonctions);

    // On ajoute l'input caché pour la liste des fonctions relative aux commissions
    function_input(newFonctions);

    // On modifie les classes du grand-parent
    CmodelField.className = 'w-field w-field--model_multiple_choice_field w-field--checkbox_select_multiple';
    FmodelField.className = 'w-field w-field--model_multiple_choice_field w-field--checkbox_select_multiple';

    // On supprime le label de l'arriere grand-parent
    Cwrapper.removeChild(Cwrapper.querySelector('label'));
    Fwrapper.removeChild(Fwrapper.querySelector('label'));

    // On lance la fonction de mise à jour au chargement de la page
    userFunctionUpdate();

    // Création du <select> pour la liste des fonctions relative aux commissions
    function function_selector(commission, value, fonction) {
        const FSELECT = document.createElement('select');
        FSELECT.classList.add("cgs-selector");
        FSELECT.setAttribute('title', commission);
        FSELECT.setAttribute('data-id', value);
        const FLABEL = document.createElement('option');
        FLABEL.value = "";
        FLABEL.selected = true;
        FLABEL.textContent = "---------";
        FSELECT.appendChild(FLABEL);
        const FMEMBRE = document.createElement('option');
        FMEMBRE.value = "3";
        FMEMBRE.textContent = "Membre";
        FSELECT.appendChild(FMEMBRE);    
        const FPRES = document.createElement('option');
        FPRES.value = "1";
        FPRES.textContent = "Président";   
        FSELECT.appendChild(FPRES); 
        const FCHARGE = document.createElement('option');
        FCHARGE.value = "2";
        FCHARGE.textContent = "Chargé de commission";
        FSELECT.appendChild(FCHARGE);
        if (fonction !== undefined) {
            FSELECT.classList.add("cgs-checked");
            FSELECT.value = fonction;   
        }
        return FSELECT;
    }

    // Création de l'input pour la liste des fonctions relative aux commissions
    function function_input(element) {
        const input = document.createElement('input');
        input.setAttribute('type', 'hidden');
        input.setAttribute('name', 'functions_commissions');
        input.setAttribute('id', 'id_functions_commissions');
        element.appendChild(input);
    } 
}

// Page de création/édition d'utilisateur, vérification du formulaire des élus
function userElectedUpdate() {
    const MUN = document.querySelector("#id_municipality");
    const FMUN = document.querySelector("#id_function_municipality");
    const CONS = document.querySelector("#id_function_council");
    const COMM = document.querySelector("#commissions-section");
    const BUR = document.querySelector("#id_function_bureau");
    const CONF = document.querySelector("#id_function_conference");
    const COMM_INPUTS = document.querySelectorAll("#id_commissions input[type='checkbox']");
    const COMM_SELECTS = document.querySelectorAll("#id_functions_commissions_list select");
    const CHARGES = document.querySelectorAll("#id_functions_commissions_list option[value='2']");

    // Désactive les sélections dans les panels spécifiés
    function initialsSelects() {        
        FMUN.classList.add("cgs-panel-disabled");
        CONS.classList.add("cgs-panel-disabled");
        BUR.classList.add("cgs-panel-disabled");
        COMM.classList.add("cgs-panel-disabled");
        CONF.classList.add("cgs-panel-disabled");
    }

    // Met à jour l'état des sélections en fonction des valeurs actuelles
    function updateSelects() {

        // Valeur "municipalité" 
        if (MUN.value) {            
            FMUN.classList.remove("cgs-panel-disabled");
        } else {
            FMUN.classList.add("cgs-panel-disabled");
            FMUN.value = "";
        }

        // Valeur "fonction municipalité" 
        if (FMUN.value) {
            CONS.classList.remove("cgs-panel-disabled");
            COMM.classList.remove("cgs-panel-disabled");
        } else {
            CONS.classList.add("cgs-panel-disabled");
            COMM.classList.add("cgs-panel-disabled");
            CONS.value = "";
            BUR.value = "";
            CONF.value = "";
            resetComm();
        }

        // Valeur "fonction conseil"
        if (CONS.value === "1") {
            CONF.value = "1";
            BUR.value = "1";
            allowCharges(false);
        } else if (CONS.value === "2") {
            CONF.value = "2";
            BUR.value = "2";
            allowCharges(true);            
        } else {
            CONF.value = (FMUN.value === "1") ? "3" : "";
            BUR.value = "";
            allowCharges(false);
        }

        function allowCharges(allow) {
            CHARGES.forEach(charge => {
                charge.disabled = !allow;
                if (!allow) {
                    charge.selected = false;
                }
            });
        }
        function resetComm() {
            COMM_INPUTS.forEach(input => {
                input.checked = false;
            });
            COMM_SELECTS.forEach(select => {
                console.log(select);
                // on remet la valeur par défaut
                select.value = "";
                select.classList.remove("cgs-checked");
            });
            userFunctionUpdate();
        }
    }

    // Ajoute des écouteurs d'événements aux sélections pour déclencher la mise à jour
    document.querySelectorAll("#id_municipality, #id_function_municipality, #id_function_council, #id_commissions").forEach(select => {
        select.addEventListener("change", updateSelects);
    });

    // Initialise l'état des sélections et applique le blocage permanent
    initialsSelects();
    updateSelects();
}

// Récupération des données de la convocation lors de la création d'un évenement Joyous
function joyousSingleEvent() {
    // Convocation
    const convocation = document.querySelector('#id_convocation');

    // Récupère l'ID de la convocation sélectionnée
    const convocationID = convocation.value;

    // Mise à jour des utilisateurs au chargement de la page, si une convocation est sélectionnée
    if (convocationID) {
        updateEventFields(convocationID);
    }

    // Mise à jour des utilisateurs lors du changement de convocation
    convocation.addEventListener('change', function () {
        const convocationId = this.value;

        if (convocationId) {
            updateEventFields(convocationId);
        }
    });

    function updateEventFields(ID) {
        fetch('/api/v2/pages/' + ID) 
            .then(response => response.json())
            .then(data => {
                // Mise à jour du titre et du slug
                const TempTitle = data.title.replace('Convocation ', '');
                const EventTitle = TempTitle.charAt(0).toUpperCase() + TempTitle.slice(1);   
                const EventSlug = TempTitle.toLowerCase().replace(/ /g, '-');             
                document.getElementById('id_title').value = EventTitle;
                document.getElementById('id_slug').value = EventSlug;

                // Mise à jour de la date
                const date = new Date(data.date); // Assurez-vous que 'data.date' est le bon format
                document.getElementById('id_date').value = formatDate(date); // Format yyyy-mm-dd
                document.getElementById('id_time_from').value = formatTime(date); // Format HH:MM

                // Mise à jour de la localisation et de l'url
                document.getElementById('id_location').value = "Hôtel communautaire. 15, avenue du Comminges 31260 MANE";
                document.getElementById('id_website').value = "https://cagiregaronnesalat.fr/"+EventSlug+"/";

                // Mise à jour de l'image           
                if (data.meta.parent.meta.logo) {
                    const logo = data.meta.parent.meta.logo;
                    updateImageFields(logo);
                }
            })
            .catch(error => console.error('Error:', error));
    }    

    function updateImageFields(logo) {
        const input = document.getElementById('id_image'); 
        const chooser = document.getElementById('id_image-chooser');
        const image = chooser.querySelector('img');        
        const title = document.getElementById('id_image-title');

        if (input) {
            input.value = logo.id;
            title.innerText = logo.title;
            image.alt = logo.title;
            image.src = logo.url;
            chooser.classList.remove("blank");
        }
    }

    function formatDate(date) {
        return date.toISOString().split('T')[0];
    }
    
    function formatTime(date) {
        return date.toTimeString().split(' ')[0].substring(0, 5);
    }
};

// Vérifications pour la page Convocation (Si la date est antérieure à la date du jour)
function convocationDate() {

    // On récupère les éléments de la page
    const DateSection = document.querySelector('#id_date');
    const agendaSection = document.querySelector('#panel-child-contenu-body-section');
    const PJSection = document.querySelector('#panel-child-contenu-pieces_jointes-section');

    if (DateSection) {
        checkConvocationDate(DateSection);
    }
    DateSection.addEventListener('change', function() {
        checkConvocationDate(this);
    });

    function checkConvocationDate(e) {
        console.log("Fonction checkConvocationDate");
        // On récupère la date de la convocation
        const DateValue = e.value;
        // On récupère la date du jour
        const today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const yyyy = today.getFullYear();
        const date = yyyy + '-' + mm + '-' + dd;
        
        // Si la date de la convocation est antérieure à la date du jour, on affiche un message d'erreur
        if (DateValue < date) {
            agendaSection.classList.add('cgs-hidden');
            const infoBlock = createInfoBlock("cv-date", "La date de la convocation est antérieure à la date du jour. Ajoutez simplement l'ancienne convocation en pièce jointe 🔗 (format PDF ou DOCX).");
            if (infoBlock) {
                PJSection.appendChild(infoBlock);        
            }
        } else {
            removeInfoBlock("cv-date");
            agendaSection.classList.remove('cgs-hidden');
        }
    }
}

// Vérifications pour la page Compte-rendu (Récupération des users de la convocation)
function compteRenduUsers() {
    // Convocation
    const convocation = document.querySelector('#id_convocation');
    
    // Secrétaire de séance
    const secretaryField = document.querySelector('#id_secretary');
    const secretarySection = document.querySelector('[data-id="secretary"]');

    // Section des absences
    const absencesSection = document.querySelector('[data-id="absences"]');

    // Absents remplacés
    const replacedUsersField = document.querySelector('#id_replaced_users');

    // Absents non remplacés
    const unreplacedUsersField = document.querySelector('#id_unreplaced_users');

    // Quorum section
    const quorumSection = document.querySelector('[data-id="quorum"]');

    // Ordre du jour
    const agendaSection = document.querySelector('[data-id="body"]');    

    // PJ
    const PJSection = document.querySelector('[data-id="attachments"]');

    // On vide les champs au chargement de la page
    secretaryField.innerHTML = '';
    replacedUsersField.innerHTML = '';
    unreplacedUsersField.innerHTML = '';

    // Récupère l'ID de la convocation sélectionnée
    const convocationID = convocation.value;

    // Mise à jour des utilisateurs au chargement de la page, si une convocation est sélectionnée
    if (convocationID) {
        updateConvocationUsers(convocationID);
    }

    // Mise à jour des utilisateurs lors du changement de convocation
    convocation.addEventListener('change', function () {
        replacedUsersField.innerHTML = '';
        unreplacedUsersField.innerHTML = '';
        const convocationId = this.value;
        if (convocationId) {
            updateConvocationUsers(convocationId);
        }
    });

    // Fonction qui crée la liste des secrétaires
    function updateSecretaryField(electedUsers, id) {
        const emptyOption = document.createElement('option');
        emptyOption.textContent = "---------";
        emptyOption.value = "";

        // On ajoute l'option vide
        secretaryField.appendChild(emptyOption);

        // On boucle sur tous les secrétaires
        electedUsers.forEach(secretary => {
            const option = document.createElement('option');
            option.value = secretary.id;
            option.textContent = secretary.name;

            // Si l'ID du secrétaire correspond à l'ID sélectionné, on le sélectionne
            if (id === secretary.id) {
                option.setAttribute('selected', 'selected');
            }
            secretaryField.appendChild(option);
        });
    }

    // Fonction qui récupère tous les utilisateurs via l'API (GET /api/v2/users/)
    function fetchUsers(callback) {
        fetch('/api/v2/users/?limit=10000')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Vérifie que la réponse contient les 'items'
                if (data && data.items) {
                    // Filtre les utilisateurs pour ne récupérer que les élus. (tous ceux qui n'ont pas "elected": "null"). 
                    // Nom de la variable dans le reste du code : electedUsers
                    const filteredUsers = data.items.filter(user => user.elected);    
                    // Appelle la fonction callback avec la liste filtrée des utilisateurs
                    callback(null, filteredUsers);
                } else {
                    // Appelle la fonction callback avec une erreur si 'items' n'est pas dans la réponse
                    callback('Items not found in response', null);
                }
            })
            .catch(error => {
                // Appelle la fonction callback avec une erreur en cas d'échec de la requête
                callback(error.message, null);
            });
    }

    // Fonction qui met à jour les champs [absents remplacés], [absents non remplacés] et [remplaçants]
    function updateUsersField(field, participants, presenceValue, electedUsers, fieldName) {
        // Déclare les variables pour les utilisateurs absents et les remplaçants
        let userIsAbsent;
        let substitutes = []; 
        let absents = [];

        // Boucle sur tous les participants liés à la Convocation
        participants.forEach((participant, index) => {
            // console.log(participant);
            const div = document.createElement('div');
            const labelUser = document.createElement('label');
            labelUser.setAttribute('for', field.id + '_' + index); 
            const inputUser = document.createElement('input');
            inputUser.setAttribute('type', 'checkbox');
            inputUser.setAttribute('name', fieldName);
            inputUser.setAttribute('value', participant.id);
            inputUser.setAttribute('sub-value', participant.user);
            inputUser.setAttribute('id', field.id + '_' + index);

            userIsAbsent = false;
            if (participant.presence === presenceValue) {
                inputUser.checked = true;
                absents.push(inputUser);
                if (electedUsers) {
                    labelUser.classList.add('cgs-checked');
                    userIsAbsent = true;
                }
            }

            labelUser.appendChild(inputUser);
            labelUser.appendChild(document.createTextNode(' ' + participant.identity));
            div.appendChild(labelUser);

            if (electedUsers) {
                let userHasAlternate = false;
                let userHasSubstitute = false;              
                let tabID = [participant.id, participant.user, false]
                const emptyOption = document.createElement('option');
                emptyOption.value = tabID;

                const selectSubstitute = document.createElement('select');
                selectSubstitute.setAttribute('name', 'substitute_users');
                selectSubstitute.setAttribute('id', 'id_substitute_users_' + index);
                selectSubstitute.appendChild(emptyOption);

                electedUsers.forEach(substitute => {
                    tabID[2] = substitute.id;
                    const option = document.createElement('option');
                    option.value = tabID;
                    option.textContent = substitute.name;
                    option.setAttribute('sub-value', substitute.id);

                    if (participant.substitute === substitute.id) {
                        if (userHasAlternate) {
                            selectSubstitute.querySelector('option:selected').removeAttribute('selected');
                            substitutes = substitutes.filter(opt => opt !== selectSubstitute.querySelector('option:selected'));
                        }
                        option.setAttribute('selected', 'selected');
                        substitutes.push(option);
                        userHasSubstitute = true;
                    }
                    if ((!userHasSubstitute) && (participant.alternate === substitute.id)) {
                        option.setAttribute('selected', 'selected');
                        substitutes.push(option);
                        userHasAlternate = true;
                    }
                    selectSubstitute.appendChild(option);
                });

                const labelSubstitute = document.createElement('label');
                labelSubstitute.setAttribute('for', 'id_' + fieldName + '_substitutes_' + index);
                labelSubstitute.appendChild(selectSubstitute);
                div.appendChild(labelSubstitute);

                if (!userHasAlternate && !userHasSubstitute) {
                    emptyOption.setAttribute('selected', 'selected');
                } else if (!userIsAbsent) {
                    emptyOption.selected = true;
                }
            }

            field.appendChild(div);
        });

        for (const abs of absents) {
            preventAbsentSubstitute(null, abs);
        }
        for (const sub of substitutes) {
            preventDuplicateSubstitute(null, sub.parentElement);
        }
    }

    // Animation (secoue + rouge)
    function nope(labelElement) {
        // Applique l'animation shake au parent du label
        const parentElement = labelElement.parentElement;
        parentElement.style.animation = 'shake 0.82s cubic-bezier(.36,.07,.19,.97) both';

        // Applique l'animation colorized au label
        labelElement.style.animation = 'colorized 0.82s ease-in-out both';

        // Réinitialise les animations à la fin
        parentElement.addEventListener('animationend', () => {
            parentElement.style.animation = '';
        });
        labelElement.addEventListener('animationend', () => {
            labelElement.style.animation = '';
        });
    }
        
    // Fonction qui active ou désactive les options de substitution dans le menu déroulant
    function substituteOptionState(enabledValue = false, disabledValue = false, excludedValue = false) {
        let optionsEnabled;
        let optionsDisabled;

        if (excludedValue) {                                
            if (enabledValue) {
                optionsEnabled = document.querySelectorAll(`option[sub-value="${enabledValue}"]:not([value="${excludedValue}"])`);
            } 
            if (disabledValue) {
                optionsDisabled = document.querySelectorAll(`option[sub-value="${disabledValue}"]:not([value="${excludedValue}"])`);
            }
        } else {
            if (enabledValue) {
                optionsEnabled = document.querySelectorAll(`option[sub-value="${enabledValue}"]`);
            } 
            if (disabledValue) {
                optionsDisabled = document.querySelectorAll(`option[sub-value="${disabledValue}"]`);
            }
        }

        // Active les options ciblées
        if (enabledValue) {
            optionsEnabled.forEach(option => {
                option.disabled = false;
            });
        }

        // Désactive les options ciblées
        if (disabledValue) {
            optionsDisabled.forEach(option => {
                option.disabled = true;
            });
        }
    }

    // Fonction qui gère l'affichage des menus déroulants pour les remplaçants
    function selectSubstituteState(event) {
        const thisInput = event.target;
        const replacedLabel = thisInput.parentElement;
        
        let blankOption = null;
        let selectedOption = null;
        if (replacedLabel.nextElementSibling) {
            blankOption = replacedLabel.nextElementSibling.querySelector("option");
            selectedOption = replacedLabel.nextElementSibling.querySelector("option[selected='selected']");
        }

        if (thisInput.checked) {
            replacedLabel.classList.add("cgs-checked");
            if (selectedOption) {
                selectedOption.selected = true; 
            }                
        } else {
            replacedLabel.classList.remove("cgs-checked");
            if (blankOption) {
                blankOption.selected = true;
            }                               
        }
    }

    // Fonction qui empêche la double sélection des absences
    function preventDuplicateCheck(event) {
        const thisInput = event.target;
        const thisName = thisInput.name;
        const thisValue = thisInput.value;

        let relatedInputSelector = thisName === "replaced_users" ? `input[name="unreplaced_users"][value="${thisValue}"]` : `input[name="replaced_users"][value="${thisValue}"]`;
        let relatedInput = document.querySelector(relatedInputSelector);

        if (relatedInput && relatedInput.checked) {
            nope(thisInput.parentElement);
            thisInput.checked = false;
            return true;
        } 

        return false;
    }

    // Fonction qui empêche de sélectionner deux fois le même remplaçant
    function preventDuplicateSubstitute(event, target) {
        let thisSelect = event ? event.target : target;
        const thisOptions = thisSelect.options;
        let enabledValue;

        for (const option of thisOptions) {
            if (option.classList.contains('cgs-selected')) {
                enabledValue = option.getAttribute('sub-value');
            }
            option.classList.remove('cgs-selected');
        }

        const thisOption = thisOptions[thisSelect.selectedIndex];
        thisOption.classList.add('cgs-selected');
        const excludedValue = thisOption.value;
        const disabledValue = thisOption.getAttribute('sub-value');

        substituteOptionState(enabledValue, disabledValue, excludedValue);
    }

    // Fonction qui empêche de sélectionner un remplaçant qui est absent
    function preventAbsentSubstitute(event, target) {
        let thisInput = event ? event.target : target;

        if (thisInput.name === "replaced_users") {
            const ID = thisInput.id;
            const select = document.getElementById(ID.replace('replaced_users', 'substitute_users'));
            preventDuplicateSubstitute(null, select);
        }

        const subValue = thisInput.getAttribute('sub-value');
        const relatedOptions = document.querySelectorAll(`option[sub-value="${subValue}"], #id_secretary option[value="${subValue}"]`);

        for (const option of relatedOptions) {
            option.disabled = thisInput.checked;
        }
    }

    // Écouteurs d'événements en fonction des champs
    function requestListener(field) {
        switch (field) {
            case 1:
                // Écouteurs pour les input "replaced"
                document.querySelectorAll('input[name="replaced_users"]').forEach(input => {
                    input.addEventListener('change', event => {
                        if (!preventDuplicateCheck(event)) {
                            selectSubstituteState(event);
                            preventAbsentSubstitute(event);
                        }
                    });
                });
                break;

            case 2:
                // Écouteurs pour les input "unreplaced"
                document.querySelectorAll('input[name="unreplaced_users"]').forEach(input => {
                    input.addEventListener('change', event => {
                        if (!preventDuplicateCheck(event)) {
                            preventAbsentSubstitute(event);
                        }
                    });
                });
                break;
            
            case 3:
                // Écouteurs pour les select "substitute_users"
                document.querySelectorAll('select[name="substitute_users"]').forEach(select => {
                    select.addEventListener('change', preventDuplicateSubstitute);
                });
                break;
        }
    }

    // 
    function oldConvocation(bool) {
        if (bool) {
            secretarySection.classList.add('cgs-hidden');
            absencesSection.classList.add('cgs-hidden');
            quorumSection.classList.add('cgs-hidden');
            agendaSection.classList.add('cgs-hidden');
            // Création du bloc d'information
            const infoBlock = createInfoBlock("cr-old", "Cette page est liée à une ancienne convocation. Ajoutez simplement le compte-rendu en pièce jointe 🔗 (format PDF ou DOCX).");
            // On l'ajoute apres le premier enfant de PJSection    
            if (infoBlock) {               
                PJSection.insertBefore(infoBlock, PJSection.firstChild.nextSibling);
            }
        } else {
            secretarySection.classList.remove('cgs-hidden');
            absencesSection.classList.remove('cgs-hidden');
            quorumSection.classList.remove('cgs-hidden');
            agendaSection.classList.remove('cgs-hidden');
            // On supprime le bloc d'information
            removeInfoBlock("cr-old");
        }
    }
    // Mise à jour des utilisateurs de la convocation
    function updateConvocationUsers(convocationId) {
        fetch('/api/v2/pages/' + convocationId + '/')
            .then(response => response.json())
            .then(data => {
                // On vérifie l'ancieneté de la convocation
                const old = data.old ? data.old : false;                
                if (old) {
                    throw new Error("Ancienne convocation détectée");
                } else {
                    oldConvocation(false);
                }
                // On récupère les participants de la convocation
                const participants = data.convocation_users ? data.convocation_users : false;

                
                // On récupere le type de parent si possible
                const parent = data.meta.parent ? data.meta.parent.meta.type : false;      
                // On récupère le secrétaire de séance si il existe
                const secretary = data.compte_rendu_page ? data.compte_rendu_page.secretary : false;
                
                if (data && parent) {                            
                    switch (parent) {                    
                        case 'administration.ConseilsIndexPage':
                            console.log("Compte-rendu de conseil détecté (on affiche tout)");
                            // On affiche les quatres sections
                            fetchUsers(function(err, electedUsers) {
                                if (err) {
                                    console.error("Erreur lors de la récupération de la liste des utilisateurs :", err);
                                    return;
                                }
                                if (data) {
                                    updateSecretaryField(electedUsers, secretary);
                                    if (participants) {
                                        updateUsersField(document.querySelector('#id_replaced_users'), participants, 2, electedUsers, "replaced_users");
                                        updateUsersField(document.querySelector('#id_unreplaced_users'), participants, 3, false, "unreplaced_users");
    
                                        requestListener(1);
                                        requestListener(2);
                                        requestListener(3);
                                    }
                                }
                            });
                            break;
                        case 'administration.BureauxIndexPage':
                            console.log("Compte-rendu de bureau détecté (on cache tout)");
                            // on cache les quatres sections, pas besoin de récupérer les participants
                            break;
                        case 'administration.CommissionPage':
                            console.log("Compte-rendu de commission détecté (on n'affiche que le secrétaire de séance)");
                            // On n'affiche que le secréatire de séance
                            fetchUsers(function(err, electedUsers) {
                                if (err) {
                                    console.error("Erreur lors de la récupération de la liste des utilisateurs :", err);
                                    return;
                                }
                
                                if (data) {
                                    updateSecretaryField(electedUsers, secretary);
                                }
                            });
                            absencesSection.classList.add('cgs-hidden');
                            quorumSection.classList.add('cgs-hidden');    
                            break;
                        case 'administration.ConferencesIndexPage':
                            console.log("Compte-rendu de conférence détecté (on affiche tout sauf le secrétaire de séance)");
                            // On n'affiche tout sauf le secrétaire de séance
                            fetchUsers(function(err, electedUsers) {
                                if (err) {
                                    console.error("Erreur lors de la récupération de la liste des utilisateurs :", err);
                                    return;
                                }
                
                                if (data && participants) {
                                        updateUsersField(document.querySelector('#id_replaced_users'), participants, 2, electedUsers, "replaced_users");
                                        updateUsersField(document.querySelector('#id_unreplaced_users'), participants, 3, false, "unreplaced_users");
    
                                        requestListener(1);
                                        requestListener(2);
                                        requestListener(3);
                                }
                            });
                            secretarySection.classList.add('cgs-hidden');
                            break;
                    }
                }
            })
            .catch(error => {
                if (error.message === "Ancienne convocation détectée") {                    
                    console.log(error.message);
                    oldConvocation(true);
                } else {
                    // Gérez ici les autres types d'erreurs
                    console.error("Erreur lors de la récupération des utilisateurs de la convocation :", error);
                }
            });   
    }
}

// On remplace les inputs (PDF et Words) par la copie du bouton pour enregistrer un brouillon
function compteRenduImportBloc() {
    const streamBlock = document.querySelector('#panel-child-contenu-body-content [data-streamfield-stream-container]');
    if (!streamBlock) {
        console.warn('StreamBlock not found');
        return;
    }

    // Fonction générale pour modifier les blocs d'importation (PDF et DOCS)
    function reworkingImportBlock(element) {
        const importBlock = (element.querySelector('[data-contentpath="pdf_import"]') || element.querySelector('[data-contentpath="docx_import"]'));
        const structBlock = importBlock.parentElement;

        // on récupere la valeur précédent le "_" du contentpath de importBlock
        const type = importBlock.dataset.contentpath.split('_')[0];

        importDisplay(structBlock, type);
        importButton(structBlock, type);
    }
        
    // Mise en page des blocs
    function importDisplay(block, type) {
        block.classList.add('cgs-colbox');
        block.querySelector(`[data-contentpath="${type}_document"]`).classList.add('cgs-column8');
        block.querySelector(`[data-contentpath="${type}_import"]`).classList.add('cgs-column4');
        const contentBloc = (block.querySelector(`[data-contentpath="pdf_images"]`) || block.querySelector(`[data-contentpath="docx_content"]`));
        contentBloc.classList.add('cgs-col12', 'cgs-collapsible', 'cgs-collapsed');
        const contentLabel = contentBloc.querySelector('label');
        contentLabel.addEventListener('click', () => collapsible(contentLabel));
    }    

    // Modification des inputs
    function importButton(bloc, type) {
        const input = bloc.querySelector(`[id^="body-"][id$="-value-${type}_import"]`);  
        const submit = document.querySelector('form#page-edit-form footer nav button[type="submit"].action-save');
        const button = submit.cloneNode(true);

        if (button) {
            button.removeChild(button.querySelector('svg.button-longrunning__icon'));
            button.classList.add('cgs-import');        
            button.dataset.wProgressLabelValue = "Importer le " + type;
            button.dataset.wProgressActiveValue = "Importation…";

            // On copie l'input et on le remplace dans le DOM par le bouton (auquel on attache un écouteur d'évenement).
            const hiddenInput = input.cloneNode(true);    
            input.replaceWith(button);

            button.addEventListener('click', function(event) {
                event.preventDefault(); // Empêcher la soumission du formulaire

                const form = button.closest('form');
                if (!form) {
                    console.log('Formulaire non trouvé');
                    return;
                }
                hiddenInput.value = "on";        
                hiddenInput.type = "hidden";   
                form.appendChild(hiddenInput);

                // Finalement on ajoute le faux formulaire au document et on le soumet
                form.submit();
            });
        }
    }

    function processImportBlocks(container) {
        // Appliquer immédiatement reworkingImportBlock à tous les éléments filtrés existants
        const initialElements = container.querySelectorAll('[data-contentpath]');
        initialElements.forEach(element => {
            if (element.querySelector('input[type="hidden"][value="PDF"], input[type="hidden"][value="DOCX"]')) {
                element.dataset.observed = true;
                reworkingImportBlock(element);
            }
        });

        // Observer les modifications pour traiter les nouveaux éléments
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1 && node.matches('[data-contentpath]')) { // ELEMENT_NODE
                        if (node.querySelector('input[type="hidden"][value="PDF"], input[type="hidden"][value="DOCX"]')) {
                            if (!node.dataset.observed) {
                                node.dataset.observed = true;
                                reworkingImportBlock(node);
                            }
                        }
                    }
                });
            });
        });

        observer.observe(container, {
            childList: true,
            subtree: true
        });
    }
    // Appliquer le traitement au streamBlock
    processImportBlocks(streamBlock);
}