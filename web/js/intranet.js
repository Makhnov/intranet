// Gestion du comportement des sous-menus pour les menus déroulants
document.addEventListener('DOMContentLoaded', function () {
    console.log("Fichier intranet.js chargé");    
    whatTheHell();
});

function whatTheHell() {    
    
    // Si le logo cgs est présent, on active les écouteurs d'événements
    const CGS = document.querySelectorAll('.logo-pochoir.right');
    if (CGS.length > 0) {
        iconColors(CGS);
    }
    
    // Ouverture et fermeture du menu utilisateur
    const PROFILE = document.querySelector('ul.profile > .avatar');
    if (PROFILE) {
        PROFILE.addEventListener('click', event => PROFILE.closest('ul').classList.toggle('cgs-open'));
    }

    // Images en plein écran
    const EXPENDABLES = document.querySelectorAll('.cgs-expandable');
    if (EXPENDABLES.length > 0) {
        expandableImages(EXPENDABLES);
    }
    
    // SWAP
    const SWAPABLES = document.querySelectorAll('.cgs-swap');
    if (SWAPABLES.length > 0) {
        swap(SWAPABLES);
    }

    // Gestion du footer
    const FOOTER = document.querySelector('footer nav.footer ul.nav-box');
    if (FOOTER) {
        footerScroll(FOOTER);
    }

    // Vague du formulaire de recherche
    const SEARCHBAR = document.getElementById('searchColumn');
    if (SEARCHBAR) {
        VerticalWave(SEARCHBAR);      
    }

    // Agrandissement de la barre de recherche
    const ZOOM = document.querySelector('cgs-search');
    if (ZOOM) {
        searchBar(ZOOM);
    }

    // Gestion de la recherche
    const FORM = document.querySelector('#searchColumn form');
    if (FORM) {
        searchBlock(FORM);
    }

    const MESSAGES = document.querySelectorAll('.cgs-message');
    if (MESSAGES.length > 0) {
        cgsMessages(MESSAGES);
    }

    const UPDATE_BLOCK = document.getElementById('update-block');
    const PROFILE_BLOCK = document.getElementById('profile-block');
    if (UPDATE_BLOCK && PROFILE_BLOCK) {
        profileUpdate(UPDATE_BLOCK, PROFILE_BLOCK);
    }
}

//////////////////////////////////////////   FONCTIONS GLOBALES    //////////////////////////////////////////////////

function cgsMessages(msgs) {
    msgs.forEach(msg => {
        const close = msg.querySelector('.msg-close');
        if (close) {
            close.addEventListener('click', () => msg.remove());
        }
    });

}

////////////////////////////////////////// PAGES/SECTION CHARGEES  //////////////////////////////////////////////////

// Fonction pour changer la couleur des icônes quand on clique sur les éléments du logo
function iconColors(divs) {
    const pochoirColors = ['#008770', '#00b3be', '#92d400', '#928b81'];

    // Fonction pour changer la couleur primary et stocker la sélection
    const changeColor = (color) => {
        document.documentElement.style.setProperty('--cgs-theme-primary', color);
        localStorage.setItem('selectedColor', color);
    };

    // Appliquez la couleur stockée (si elle existe)
    const storedColor = localStorage.getItem('selectedColor');
    if (storedColor) {
        changeColor(storedColor);
    }

    // Gestionnaire d'événements pour chaque div
    divs.forEach((div, index) => {
        div.addEventListener('click', (event) => {
            // Empêchez l'ouverture du lien <a>
            event.preventDefault();

            // Changer la couleur primary et stocker la sélection
            changeColor(pochoirColors[index]);
        });
    });
}

// Fonction pour afficher les images en plein écran
function expandableImages(images) {
    images.forEach(img => {
        img.addEventListener('click', function() {
            const fullscreenDiv = document.createElement('div');
            fullscreenDiv.classList.add('cgs-fullscreen-container');
    
            const cloneImg = this.cloneNode();
            fullscreenDiv.appendChild(cloneImg);

            document.body.appendChild(fullscreenDiv);
    
            fullscreenDiv.addEventListener('click', function() {
                this.remove();
            });
        });
    });
}

// Fonction pour gérer les éléments permutables
function swap(swapables) {

    function hideSwapable(smooth=false, direction=false, element) {
        if (smooth) {
            if (direction) {        
                element.classList.toggle('cgs-width-none');
            } else {
                element.classList.toggle('cgs-height-none');
            }
        } else {
            element.classList.toggle('cgs-hidden');
        }
    }

    for (const swapable of swapables) {
        const swaper = swapable.querySelector('.cgs-swapable');
        const icons = swaper.querySelectorAll('svg, img');
        const heading = swapable.querySelector('p.cgs-heading');
        // On récupère les deux icones on affiche le bon (valeur du title)      
        const primaryIcon = icons[0];
        const secondaryIcon = icons[1];
        // On récupèes les infos : Smooth (true/false) et width/height (widht true/false)
        const smooth = swaper.getAttribute('data-smooth');
        const horizontal = swaper.getAttribute('data-width');

        if (swaper.title == "Masquer") {
            primaryIcon.classList.add('cgs-hidden');
        } else {
            secondaryIcon.classList.add('cgs-hidden');
        }

        // Sélection du prochain élément cgs-hidden
        let next = swapable.nextElementSibling;
        while (next) {
            if (next.classList.contains('cgs-swap-visible')) {
                next.classList.remove('cgs-swap-visible');
                break;
            } else if (next.classList.contains('cgs-swap-hidden')) {
                next.classList.remove('cgs-swap-hidden');
                hideSwapable(smooth, horizontal, next);
                break;
            }            
            next = next.nextElementSibling;
        }

        swaper.addEventListener('click', function () {
            primaryIcon.classList.toggle('cgs-hidden');
            secondaryIcon.classList.toggle('cgs-hidden');
            hideSwapable(smooth, horizontal, next);
            
            // Changement du titre pour le tooltip
            if (swaper.getAttribute('title') === 'Afficher') {
                swaper.setAttribute('title', 'Masquer');                
                if (heading) {
                    const newContent = heading.textContent.replace('Afficher', 'Masquer');                    
                    heading.textContent = newContent;
                }
            } else {
                swaper.setAttribute('title', 'Afficher');
                if (heading) {
                    const newContent = heading.textContent.replace('Masquer', 'Afficher');                    
                    heading.textContent = newContent;
                }
            }
        });
    }
}

// Navigation dans le menu du bas < et >
function footerScroll(footerBox) {

    const styling = getComputedStyle(document.body);
    const footerLeft = document.querySelector('footer nav.footer div.cgs-box.left');
    const footerRight = document.querySelector('footer nav.footer div.cgs-box.right');
    const footerIconMargin = parseFloat(styling.getPropertyValue('--nav-icon-margin'));
    const footerIconwidth = parseFloat(styling.getPropertyValue('--nav-icon-size'));
    const scrollAmount = 32 * (1.5 * footerIconMargin + footerIconwidth);

    // Visibilité des chevrons
    const updateFooterArrows = () => {
        if (footerBox.scrollLeft === 0) {
        footerLeft.classList.add('cgs-hidden');
        } else {
        footerLeft.classList.remove('cgs-hidden');
        }

        if (footerBox.scrollLeft + footerBox.offsetWidth >= footerBox.scrollWidth) {
            footerRight.classList.add('cgs-hidden');
        } else {
            footerRight.classList.remove('cgs-hidden');
        }
    };

    // Fonction pour défiler vers la gauche
    footerLeft.addEventListener('click', () => {
        footerBox.scrollLeft -= scrollAmount;
    });

    // Fonction pour défiler vers la droite
    footerRight.addEventListener('click', () => {
        footerBox.scrollLeft += scrollAmount;
    });

    // Mettre à jour la visibilité des chevrons après le défilement
    footerBox.addEventListener('scroll', updateFooterArrows);

    // Récupérer la position de défilement enregistrée
    const savedScrollPosition = localStorage.getItem('footerScrollPosition');
    if (savedScrollPosition !== null) {
        footerBox.scrollLeft = parseInt(savedScrollPosition);
    }

    // Initialiser la visibilité des chevrons au chargement et au resize
    updateFooterArrows();
    window.addEventListener('resize', updateFooterArrows);

    // Enregistrer la position de défilement lors de la fermeture de la fenêtre
    window.addEventListener('beforeunload', () => {
        localStorage.setItem('footerScrollPosition', footerBox.scrollLeft);
    });
}

// Mise en forme de la vague du formulaire de recherche
function VerticalWave(search) {
    const resizeObserver = new ResizeObserver(waveForm);
    resizeObserver.observe(search);  

    function waveForm() {
        const width = search.offsetWidth;
        const height = search.offsetHeight;

        const Yscale = 1.1 / (160 / width);
        const Xscale = 1 / (800 / height);

        document.documentElement.style.setProperty('--courbure-scaling-x', Xscale);
        document.documentElement.style.setProperty('--courbure-scaling-y', Yscale);
    }
}

// Fonction pour ouvrir et fermer la barre de recherche
function searchBar(searchBox) {
    searchButtons = searchBox.children;
    const searchBase = searchButtons[0];
    const searchOut = searchButtons[1];
    const searchIn = searchButtons[2];

    const searchBar = document.querySelector('cgs-search > form > input');

    searchBase.addEventListener('click', () => {
        searchBase.classList.add('cgs-hidden');
        searchOut.classList.remove('cgs-hidden');
        searchBar.classList.add('cgs-open');
        searchBox.classList.add('cgs-open');
    });
    searchOut.addEventListener('click', () => {
        searchOut.classList.add('cgs-hidden');
        searchIn.classList.remove('cgs-hidden');
        searchBar.classList.remove('cgs-open');
        searchBox.classList.remove('cgs-open');
    });
    searchIn.addEventListener('click', () => {
        searchIn.classList.add('cgs-hidden');
        searchOut.classList.remove('cgs-hidden');
        searchBar.classList.add('cgs-open');
        searchBox.classList.add('cgs-open');
    });
    searchBar.addEventListener('focus', () => {
        searchBar.classList.add('cgs-open');
        searchBase.classList.add('cgs-hidden');
        searchIn.classList.add('cgs-hidden');
        searchOut.classList.remove('cgs-hidden');
        searchBox.classList.add('cgs-open');
    });
}

// Gestion de la zone de recherche (vague verticale)
function searchBlock(form) {

    ////////////////// INITIALISATION DES VARIABLES ////////////////////

    const urlParams = new URLSearchParams(window.location.search);
    const activeCategoryDiv = document.getElementById('activeCategory');    
    const categoryName = activeCategoryDiv.getAttribute('data-name');
    const selectedCategory = urlParams.get(categoryName);
    const categoryButtons = document.querySelectorAll(`input[name="${categoryName}"]`);
    const selectedTags = urlParams.getAll('tag');
    const selectedQuery = urlParams.get('query');
    const selectedDate = [urlParams.get('start_date'), urlParams.get('end_date')];
    const categoryLabel = activeCategoryDiv.getAttribute('data-nom');
    const tagButtons = document.querySelectorAll('.tag-button');
    const CGSFORM = document.getElementById('cgs-search-form');
    const activeTagsDiv = document.getElementById('activeTags');
    const activeQueryDiv = document.getElementById('activeQuery');
    const activeDateDiv = document.getElementById('activeDate');

    ///////////////////// ECOUTEURS D'EVENEMENTS ///////////////////////

    // Choix d'une catégorie
    if (categoryButtons) {
        categoryButtons.forEach(radio => {
            radio.addEventListener('change', function() {
                submitForm();
            });
        }); 
    }
        
    // Ajout d'un tag par les tags populaires
    if (tagButtons) {
        tagButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tagName = this.getAttribute('data-tag');
                addTag(tagName);
                submitForm();
            });
        });
    }

    // Une recherche a été faite (automatique pour les FAQS)
    console.log("Category :", (selectedCategory), "Tags :", selectedTags, "Query :", selectedQuery, "Date :", selectedDate);    
    if (selectedCategory || selectedTags.length > 0 || selectedQuery || selectedDate[0] || selectedDate[1]) {
    
        // Afficher la catégorie active
        if (selectedCategory) {
            // ajout d'un bouton cliquable (pour supprimer la catégorie en cours et sélectionner automatiquement "toutes")
            const div = document.createElement('div');        
            const svg = document.querySelector('#cgs-close svg').cloneNode(true);
            const span = document.createElement('span');
            svg.id = 'svg_close_categorie';
            svg.classList.add('cgs-small-icon', 'cgs-close');
            svg.onclick = function() {
                categoryButtons.forEach(radio => {
                    radio.checked = false;
                });
                submitForm();
            };
            span.textContent = `${categoryLabel} : ${selectedCategory}`;
            div.appendChild(span);
            div.appendChild(svg);
            activeCategoryDiv.appendChild(div);
        } else {
            console.log('ELSE')
            const div = document.createElement('div');
            const span = document.createElement('span');
            span.textContent = `${categoryLabel} : Toutes`;
            div.appendChild(span);
            activeCategoryDiv.appendChild(div);
        }
    
        // Afficher la recherche active
        if (selectedQuery) {
            const div = document.createElement('div');
            const svg = document.querySelector('#cgs-close svg').cloneNode(true);
            const span = document.createElement('span');
        
            svg.id = 'svg_close_query';
            svg.classList.add('cgs-small-icon', 'cgs-close');
            svg.onclick = function() {
                const queryInput = document.querySelector('input[name="query"]');
                queryInput.value = '';
                console.log(queryInput.value);
                submitForm();
            };
            span.textContent = `Recherche : ${selectedQuery}`;
            div.appendChild(span);
            div.appendChild(svg);
            activeQueryDiv.appendChild(div);
        }

        // Afficher les tags actifs
        if (selectedTags.length > 0) {
            // Afficher les tags actifs
            selectedTags.forEach(tagName => addTag(tagName));    
        }

        // Afficher la date de début
        if (selectedDate[0]) {
            const div = document.createElement('div');
            const span = document.createElement('span');
            const svg = document.querySelector('#cgs-close svg').cloneNode(true);
            svg.id = 'svg_close_start_date';
            svg.classList.add('cgs-small-icon', 'cgs-close');
            svg.onclick = function() {
                const startDateInput = document.querySelector('input[name="start_date"]');
                startDateInput.value = '';
                submitForm();
            };
            span.textContent = `Début : ${selectedDate[0]}`;
            div.appendChild(span);
            div.appendChild(svg);
            activeDateDiv.appendChild(div);
        }

        // Afficher la date de fin
        if (selectedDate[1]) {
            const div = document.createElement('div');
            const span = document.createElement('span');
            const svg = document.querySelector('#cgs-close svg').cloneNode(true);
            svg.id = 'svg_close_end_date';
            svg.classList.add('cgs-small-icon', 'cgs-close');
            svg.onclick = function() {
                const endDateInput = document.querySelector('input[name="end_date"]');
                endDateInput.value = '';
                submitForm();
            };
            span.textContent = `Fin : ${selectedDate[1]}`;
            div.appendChild(span);
            div.appendChild(svg);
            activeDateDiv.appendChild(div);
        }

    }

    /////////////////////// FONCTIONS DIVERSES /////////////////////////

    // Ajout d'un tag en utilisant les tags personnalisés
    function addTag(tagName) {
        if (![...activeTagsDiv.children].some(tagDisplay => tagDisplay.textContent.startsWith(tagName))) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'tag';
            input.value = tagName;
            CGSFORM.appendChild(input);
    
            // Créer un div pour le tag actif
            const div = document.createElement('div');
            div.className = 'active-tag-div'; // ajouter une classe pour le style si nécessaire
            
            // Créer un span pour le texte du tag
            const span = document.createElement('span');
            span.textContent = tagName;
    
            // Cloner et préparer le SVG pour le bouton de suppression
            const svg = document.querySelector('#cgs-close svg').cloneNode(true);
            svg.id = 'svg_close_' + tagName; // Assurez-vous que l'ID est unique
            svg.classList.add('cgs-small-icon', 'cgs-close');
            svg.onclick = function() {
                CGSFORM.removeChild(input); // Retirer l'input caché
                activeTagsDiv.removeChild(div); // Retirer le div du tag actif
                submitForm(); // Resoumettre le formulaire pour mettre à jour les résultats
            };
    
            // Assembler le div du tag actif
            div.appendChild(span);
            div.appendChild(svg);
            activeTagsDiv.appendChild(div);
        }
    }

    // Soumission du formulaire
    function submitForm() {
        CGSFORM.submit();
    }        
}

// Modification des informations personnelles
function profileUpdate(updateBox, profileBox) {
    const query = window.location.search;
    const urlParams = new URLSearchParams(query);

    if (urlParams.get('form') === 'true') {
        updateBox.classList.remove('cgs-hidden');
        profileBox.classList.add('cgs-hidden');
        avatarToggle();
    } else {
        updateBox.classList.add('cgs-hidden');
        profileBox.classList.remove('cgs-hidden');
        avatarToggle();
    }
}

// Toggle d'avatar
function avatarToggle() {
    const clearAvatar = document.getElementById('clear_avatar');
    const previewAvatar = document.getElementById('preview_avatar');

    if (clearAvatar && previewAvatar) {
        clearAvatar.addEventListener('click', function() {
            const defaultSrc = previewAvatar.getAttribute('data-default');
            const currentSrc = previewAvatar.getAttribute('data-current');
            console.log(clearAvatar.checked);
            
            if (clearAvatar.checked) {
                if (defaultSrc === currentSrc) {
                    alert("🚫 Vous utilisez déjà l'avatar par défaut, il n'y a rien à réinitialiser.");
                    clearAvatar.checked = false;
                } else {
                    previewAvatar.src = defaultSrc;
                }
            } else {
                previewAvatar.src = currentSrc;
            }
        });
    }
}
