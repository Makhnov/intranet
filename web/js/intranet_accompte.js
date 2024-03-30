document.addEventListener('DOMContentLoaded', function() {
    accountType();
});

// Fonction de routage lors du chargement d'une page
function accountType() {
    const TYPE = document.body ? document.body.getAttribute('class') : '';
    const inputPass = document.querySelectorAll('input[type="password"]');
    
    // Inputs (visibles / cachés)
    if (inputPass.length > 0) {
        eye(inputPass);
    }

    // Page de connexion
    if (TYPE.includes("login")) {
        console.log("Page de connexion détectée");
        login();
    }

    // Page de changement de mot de passe (si type = password & type = change)
    if (TYPE.includes("password") && TYPE.includes("change")) {
        console.log("Page de changement de mot de passe détectée");
        change();
    }
}

////////////////////////////////////////// FONCTIONS GLOBALES //////////////////////////////////////////////////

function eye(inputs) {
    inputs.forEach(function(input) {
        // Créer un élément span pour l'oeil
        // <span class="cgs-eye showpass"></span>
        const eye = document.createElement('span');
        eye.classList.add('cgs-eye', 'showpass');
        input.insertAdjacentElement('afterend', eye);        
        
        // Ecouteur d'évenement sur l'oeil
        eye.addEventListener('click', function() {
            // Changement d'état
            this.classList.toggle('showpass');
            if (this.classList.contains('showpass')) {
                input.setAttribute('type', 'password');
            } else {
                input.setAttribute('type', 'text');
            }
        });
    });
}

//////////////////////////////////////////    PAGES CHARGEES  //////////////////////////////////////////////////

// Page de connexion
function login() {

    // Sélectionner les champs de formulaire username et password
    const usernameInput = document.getElementById('id_username');
    const loginInput = document.getElementById('id_login');
    const passwordInput = document.getElementById('id_password');

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

// Page de changement de mot de passe
function change() {
    // On récupère le <ul> dans le formulaire pour le placer apres le premier <p>
    const MAIN = document.querySelector('main');
    const H2 = MAIN.querySelector('h2');
    const FORM = document.querySelector('form');
    const UL = FORM.querySelector('ul:not(.errorlist)');
    UL.classList.add('cgs-hidden');

    const DIV = document.createElement('div');
    DIV.classList.add('cgs-form-block', 'cgs-closed', 'info');

    const A = document.createElement('a');
    A.classList.add('icon', 'icon-plus-inverse', 'icon-larger');
    A.setAttribute('ID', 'rules-dropdown');
    A.setAttribute('alt', 'Ouvrir le menu déroulant des règles de mot de passe');
    A.setAttribute('title', 'Afficher les règles relatives aux mots de passe');

    const text = document.createElement('strong');
    text.textContent = "Voir les règles relatives aux mots de passe";
    const icon = document.createElement('span');
    icon.textContent ="🔐"
    //🔽▶️      
    
    A.appendChild(text); 
    A.appendChild(icon); 
    DIV.appendChild(A);
    DIV.appendChild(UL);
    MAIN.insertBefore(DIV, H2.nextSibling);

    A.addEventListener('click', function() {
        UL.classList.toggle('cgs-hidden');
        DIV.classList.toggle('cgs-closed');
        if (UL.classList.contains('cgs-hidden')) {
            icon.textContent = "🔐";
            A.setAttribute('title', 'Afficher les règles relatives aux mots de passe');
            A.setAttribute('alt', 'Ouvrir le menu déroulant des règles de mot de passe');
        } else {
            icon.textContent = "🔓";
            A.setAttribute('title', 'Masquer les règles relatives aux mots de passe');
            A.setAttribute('alt', 'Fermer le menu déroulant des règles de mot de passe');
        }
    });

    const ERRORS = document.querySelectorAll('ul.errorlist');
    console.log(ERRORS);

    ERRORS.forEach(function(err) {
        console.log(err)

        let nextP = err.nextElementSibling;
        while (nextP && nextP.tagName !== 'P') {
            nextP = nextP.nextElementSibling;
        }

        console.log(nextP);

        if (nextP && nextP.tagName === 'P') {
            // Déplacer errorList pour qu'il soit juste après ce <p>
            if (nextP.nextElementSibling) {
                nextP.parentNode.insertBefore(err, nextP.nextElementSibling);
            } else {
                // Si le <p> est le dernier enfant, ajouter errorList à la fin du parent
                nextP.parentNode.appendChild(err);
            }
        }
    });
}