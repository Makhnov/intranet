document.addEventListener('DOMContentLoaded', function() {
    whereAmI();
});

// Fonction de routage lors du chargement d'une page
function whereAmI() {
    const bodyClass = document.body ? document.body.getAttribute('class') : '';
    const header = document.querySelector('header');
    const headerText = header && header.querySelector('h1') ? header.querySelector('h1').textContent : '';    
    console.log(bodyClass);

    // Page de connexion
    if (bodyClass.includes("login")) {
        console.log("Page de connexion détectée");
        login();
    }

    // Page d'accueil du Dashboard
    if (bodyClass.includes("homepage")) {
        console.log("Page d'accueil du Dashboard détectée");
        accueil();
    }

    // Pages de l'Amicale (création et édition)
    if (document.querySelector('#id_use_map')) {
        console.log("Page de l'amicale détectée");
        amicale();
    }

    // Page intermédiaire de la création de Convocs ou de CR en passant par Quickcreate (page d'accueil)
    if (document.querySelector('body.ready ul.listing.cgs-quick')) {
        console.log("Page quickcreate détectée");
        quickcreate();
    }

    // Page des FAQ (listes de toutes les questions)
    if (headerText.includes('Agents') && header.closest('header').classList.contains('w-slim-header')) {
        console.log("Page de FAQ détectée");
        faq();
    }

    // Page de listing des utilisateurs
    if (document.querySelector("#listing-results.users")) {
        console.log("Page d'affichage des utilisateurs détectée");
        list_users();
    }

    // Page de création/édition d'utilisateur, vérification du formulaire des élus
    if (document.querySelector("form[action^='/admin/users/'][method='post']")) {
        console.log("Création/édition d'utilisateur détectée");
        edit_users_elected();
    }

    // Page de création/édition d'un évènmenet joyous (formulaire action contient joyous/simpleeventpage/)
    if (document.querySelector("form[action*='joyous/simpleeventpage/'][method='post']")) {
        console.log("Création/édition d'évènement détectée");
        single_event();
    }

    // Vérifications pour la page Compte-rendu (Récupération des users de la convocation)
    if (headerText.includes('Compte-rendu') && header.closest('header').classList.contains('w-slim-header')) {
        console.log("Page de compte-rendu détectée");
        compteRendu();
    }
}

// Page de connexion
function login() {

    // Sélectionner le span avec l'icone hide/show du formulaire
    const eye = document.querySelector('span.cgs-eye');

    // Sélectionner les champs de formulaire username et password
    const usernameInput = document.getElementById('id_username');
    const loginInput = document.getElementById('id_login');
    const passwordInput = document.getElementById('id_password');

    // Ecouteur d'évenement sur l'oeil
    eye.addEventListener('click', function() {
        // Changement d'état
        this.classList.toggle('cgs-hidden');
        if (this.classList.contains('cgs-hidden')) {
            passwordInput.setAttribute('type', 'password');
        } else {
            passwordInput.setAttribute('type', 'text');
        }
    });

    // Sélectionner le faux bouton de soumission du formulaire
    const fakeSubmit = document.querySelector('.form-actions div.fake');

    // Sélectionner tous les champs input dans le formulaire avec la classe 'cgs-content-block'
    const inputs = document.querySelectorAll('.w-field__input input');

    // Fonction pour vérifier la valeur de tous les inputs
    function checkFilled() {
        const filled = Array.from(inputs).every(input => input.value !== '');
        fakeSubmit.style.zIndex = filled ? '-1' : '2';
    }

    // Ajouter des écouteurs d'événements pour chaque input
    inputs.forEach(function(input) {

        // Fonction pour vérifier la valeur de l'input        
        function checkInputValue(thisInput) {
            if (thisInput.value !== '') {
                thisInput.closest('.cgs-form-block').classList.add('cgs-input');
            } else {
                thisInput.closest('.cgs-form-block').classList.remove('cgs-input');
            }
            // Vérifier l'état de tous les inputs après chaque modification
            checkFilled();
        }
        
        // Écouteur pour le focus
        input.addEventListener('focus', function() {
            this.closest('.cgs-form-block').classList.add('cgs-focus');
        });

        // Écouteur pour le défocus (blur)
        input.addEventListener('blur', function() {
            this.closest('.cgs-form-block').classList.remove('cgs-focus');
        });

        // Écouteur pour les changements de valeur
        input.addEventListener('input', function() {
            checkInputValue(this);
        });

        // Vérifier les valeurs initiales
        checkInputValue(input);
    });

    // Empêcher la soumission du formulaire si l'un des champs est vide avec animation
    fakeSubmit.addEventListener('click', function() {

        // Vérifier si les champs sont vides et appliquer l'animation si nécessaire
        let isFormValid = true;
        if (usernameInput !== null && !usernameInput.value.trim()) {
            nope(usernameInput.closest('.cgs-form-block'));
            isFormValid = false;
        } else if (loginInput !== null && !loginInput.value.trim()) {
            nope(loginInput.closest('.cgs-form-block'));
            isFormValid = false;
        }
        if (!passwordInput.value.trim()) {
            nope(passwordInput.closest('.cgs-form-block'));
            isFormValid = false;
        }
    });

    // Fonction nope (pour secouer et changer la couleur)
    function nope(element) {

        // Applique l'animation shake au container
        element.style.animation = 'shake 0.82s cubic-bezier(.36,.07,.19,.97) both';
        // Applique l'animation colorized au label
        element.firstElementChild.style.animation = 'colorized 0.82s ease-in-out both';

        function handleAnimationEnd() {
            element.style.animation = '';
            element.removeEventListener('animationend', handleAnimationEnd);
            element.firstElementChild.style.animation = '';
            element.firstElementChild.removeEventListener('animationend', handleAnimationEnd);
        }
    
        element.addEventListener('animationend', handleAnimationEnd);
    }
}

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
    let commissionLinks = [];
    document.querySelectorAll('body.ready ul.listing li a').forEach(function(link) {
        if (link.innerHTML.includes('Commissions &gt;')) {
            commissionLinks.push({
                href: link.getAttribute('href'),
                text: link.querySelector('strong').textContent
            });
            link.parentElement.remove();
        } else {
            link.innerHTML = link.querySelector('strong').outerHTML;
        }
    });

    if (commissionLinks.length) {
        let dropdownHtml = '<li><a class="icon icon-plus-inverse icon-larger toggle-commissions hidden"><strong>Commissions</strong></a><ul id="commissions" class="hidden">';
        commissionLinks.forEach(function(link) {
            dropdownHtml += `<li><a href="${link.href}">${link.text}</a></li>`;
        });
        dropdownHtml += '</ul></li>';

        document.querySelector('body.ready ul.listing').insertAdjacentHTML('beforeend', dropdownHtml);
    }

    document.querySelectorAll('.toggle-commissions').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.getElementById('commissions').classList.toggle('hidden');
            btn.classList.toggle('hidden');
        });
    });
}

// Page des FAQ (listes de toutes les questions)
function faq() {
    // On boucle sur les <a> du thead pour modifier le titre
    const As = document.querySelectorAll("thead th a");
    As.forEach(a => {        
        if (a.title.includes("Titre")) {
            a.textContent = `${a.textContent}: [Thématique] - [Cibles] - [Mots-clef]`;
        }
    });
}

// Page de listing des utilisateurs
function list_users() {
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

// Page de création/édition d'utilisateur, vérification du formulaire des élus
function edit_users_elected() {
    // Liste des identifiants des panels à gérer
    const CGSPanels = ["conference", "commission", "council"];

    // Désactive les sélections dans les panels spécifiés
    function disableSelects() {
        CGSPanels.forEach(name => {
            document.querySelectorAll(`#${name}-content select`).forEach(select => select.classList.add("cgs-panel-disabled"));
        });
    }

    // Bloque de manière permanente certaines sélections spécifiques
    function permanentLockedSelects() {
        document.querySelector("#id_function_conference").classList.add("cgs-panel-disabled");
        document.querySelector("#id_function_bureau").classList.add("cgs-panel-disabled");
    }

    // Réinitialise les valeurs des sélections en fonction des valeurs des autres sélections
    function resetSelectsValues() {
        const municipalityValue = document.querySelector("#id_function_municipality").value;
        const councilValue = document.querySelector("#id_function_council").value;

        if (municipalityValue === "") {
            document.querySelector("#id_function_council").value = "";
            // Réinitialise les sélections suivantes si la valeur de la municipalité est vide
            document.querySelector("#id_commission").value = "";
            document.querySelector("#id_function_commission").value = "";
            document.querySelector("#id_function_bureau").value = "";
            document.querySelector("#id_function_conference").value = "";
        }
        
        if (councilValue === "") {
            // Réinitialise les sélections de la commission si la valeur du conseil est vide
            document.querySelector("#id_commission").value = "";
            document.querySelector("#id_function_commission").value = "";
        }
    }

    // Met à jour l'état des sélections en fonction des valeurs actuelles
    function updateSelects() {
        // Récupère les valeurs actuelles des sélections principales
        const municipalityValue = document.querySelector("#id_function_municipality").value;
        const councilValue = document.querySelector("#id_function_council").value;
        const commissionValue = document.querySelector("#id_commission").value;

        // Gère la désactivation des options spécifiques de la commission
        const functionCommissionOptions = document.querySelector("#id_function_commission").options;
        if (councilValue !== "2") {
            functionCommissionOptions[2].disabled = true;
        } else {
            functionCommissionOptions[2].disabled = false;
        }

        // Gère l'activation ou la désactivation de la sélection de la commission
        const idCommission = document.querySelector("#id_commission");
        if (["1", "2", "3"].includes(councilValue)) {
            idCommission.classList.remove("cgs-panel-disabled");
        } else {
            idCommission.classList.add("cgs-panel-disabled");
        }

        // Gère l'état de la sélection de la fonction de la commission
        const idFunctionCommission = document.querySelector("#id_function_commission");
        if (commissionValue === "") {
            idFunctionCommission.classList.add("cgs-panel-disabled");
        } else {
            idFunctionCommission.classList.remove("cgs-panel-disabled");
        }

        // Ajuste les valeurs des sélections bureau et conférence en fonction des autres sélections
        const idFunctionBureau = document.querySelector("#id_function_bureau");
        idFunctionBureau.value = councilValue === "1" ? "1" : (councilValue === "2" ? "2" : "");

        const idFunctionConference = document.querySelector("#id_function_conference");
        if (councilValue === "1") {
            idFunctionConference.value = "1";
        } else if (councilValue === "2") {
            idFunctionConference.value = "2";
        } else {
            idFunctionConference.value = municipalityValue === "1" ? "3" : "";
        }

        // Gère l'affichage des panels en fonction des valeurs de municipalité et de conseil
        if (municipalityValue === "") {
            disableSelects();
        } else if (["1", "2", "3"].includes(municipalityValue)) {
            const conferenceContentHidden = document.querySelector("#conference-content-hidden");
            const conferenceContent = document.querySelector("#conference-content");
            if (["1", "2"].includes(councilValue) || municipalityValue === "1") {
                conferenceContentHidden.classList.add("cgs-panel-hidden");
                conferenceContent.classList.remove("cgs-panel-hidden");
            } else {
                conferenceContentHidden.classList.remove("cgs-panel-hidden");
                conferenceContent.classList.add("cgs-panel-hidden");
            }
            document.querySelector("#id_function_council").classList.remove("cgs-panel-disabled");
        }
        
        resetSelectsValues();
    }

    // Ajoute des écouteurs d'événements aux sélections pour déclencher la mise à jour
    document.querySelectorAll("#id_function_municipality, #id_function_council, #id_commission").forEach(select => {
        select.addEventListener("change", updateSelects);
    });

    // Initialise l'état des sélections et applique le blocage permanent
    updateSelects();
    permanentLockedSelects();
}

// Récupération des données de la convocation lors de la création d'un évenement Joyous
function single_event() {
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
        // console.log("update ID", ID);
        fetch('/api/v2/pages/' + ID) 
            .then(response => response.json())
            .then(data => {
                // console.log(data);
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

// Vérifications pour la page Compte-rendu (Récupération des users de la convocation)
function compteRendu() {
    // Convocation
    const convocation = document.querySelector('#id_convocation');
    
    // Secrétaire de séance
    const secretaryField = document.querySelector('#id_secretary');

    // Absents remplacés
    const replacedUsersField = document.querySelector('#id_replaced_users');

    // Absents non remplacés
    const unreplacedUsersField = document.querySelector('#id_unreplaced_users');

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
                    // Filtre les utilisateurs pour exclure ceux qui ont "elected": "empty"
                    const filteredUsers = data.items.filter(user => user.elected !== "empty");
                    
                    // Appelle la fonction callback avec la liste filtrée des utilisateurs
                    console.log("filteredUsers", filteredUsers)
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
    function updateUsersField(field, users, presenceValue, electedUsers, fieldName) {
        // Déclare les variables pour les utilisateurs absents et les remplaçants
        let userIsAbsent;
        let substitutes = []; 
        let absents = [];

        // Boucle sur tous les participants liés à la Convocation
        users.forEach((user, index) => {
            const div = document.createElement('div');
            const labelUser = document.createElement('label');
            labelUser.setAttribute('for', field.id + '_' + index); 
            const inputUser = document.createElement('input');
            inputUser.setAttribute('type', 'checkbox');
            inputUser.setAttribute('name', fieldName);
            inputUser.setAttribute('value', user.id);
            inputUser.setAttribute('sub-value', user.user);
            inputUser.setAttribute('id', field.id + '_' + index);

            userIsAbsent = false;
            if (user.presence === presenceValue) {
                inputUser.checked = true;
                absents.push(inputUser);
                if (electedUsers) {
                    labelUser.classList.add('cgs-checked');
                    userIsAbsent = true;
                }
            }

            labelUser.appendChild(inputUser);
            labelUser.appendChild(document.createTextNode(' ' + user.identity));
            div.appendChild(labelUser);

            if (electedUsers) {
                let userHasAlternate = false;
                let userHasSubstitute = false;              
                let tabID = [user.id, user.user, false]
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

                    if (user.substitute === substitute.id) {
                        if (userHasAlternate) {
                            selectSubstitute.querySelector('option:selected').removeAttribute('selected');
                            substitutes = substitutes.filter(opt => opt !== selectSubstitute.querySelector('option:selected'));
                        }
                        option.setAttribute('selected', 'selected');
                        substitutes.push(option);
                        userHasSubstitute = true;
                    }
                    if ((!userHasSubstitute) && (user.alternate === substitute.id)) {
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

    // Mise à jour des utilisateurs de la convocation
    function updateConvocationUsers(convocationId) {
        fetchUsers(function(err, electedUsers) {
            console.log("electedUsers", electedUsers);
            if (err) {
                console.error("Erreur lors de la récupération de la liste des utilisateurs :", err);
                return;
            }

            fetch('/api/v2/pages/' + convocationId + '/')
                .then(response => response.json())
                .then(data => {
                    if (data && data.convocation_users) {
                        const secretary = data.compte_rendu_page ? data.compte_rendu_page.secretary : false;
                        updateSecretaryField(electedUsers, secretary);
                        updateUsersField(document.querySelector('#id_replaced_users'), data.convocation_users, 2, electedUsers, "replaced_users");
                        updateUsersField(document.querySelector('#id_unreplaced_users'), data.convocation_users, 3, false, "unreplaced_users");

                        requestListener(1);
                        requestListener(2);
                        requestListener(3);
                    }
                })
                .catch(error => {
                    console.error("Erreur lors de la récupération des utilisateurs de la convocation :", error);
                });
        });
    }
}