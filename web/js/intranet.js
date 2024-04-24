// Gestion du comportement des sous-menus pour les menus déroulants
document.addEventListener('DOMContentLoaded', function () {
    CGSTheme(USER_THEME, USER_ICONS, USER_AVATAR);
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
    
    // Preview (texte en plein écran)
    const PREVIEWS = document.querySelectorAll('.cgs-preview');
    if (PREVIEWS.length > 0) {
        preview(PREVIEWS);
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

    // Agrandissement de la barre de recherche
    const NEWS = document.querySelector('cgs-news');
    if (NEWS) {
        newsBlock(NEWS);
    }

    // Gestion de la zone de recherche
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

function CGSTheme(theme, icons, avatar) {
    if (!sessionStorage.getItem('selectedColor')) {
        const defaultColor = CGS_COLORS[icons];
        document.documentElement.style.setProperty('--cgs-theme-primary', defaultColor);
        console.log('Couleur appliquée par défaut:', defaultColor);
    } else {
        const sessionColor = sessionStorage.getItem('selectedColor');
        document.documentElement.style.setProperty('--cgs-theme-primary', sessionColor);
        console.log('Couleur appliquée depuis sessionStorage:', sessionColor);
    }
}

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
    // Fonction pour changer la couleur primary et stocker la sélection
    const changeColor = (color) => {
        document.documentElement.style.setProperty('--cgs-theme-primary', color);
        sessionStorage.setItem('selectedColor', color); // Utilisation de sessionStorage pour la durée de la session
    };

    // Gestionnaire d'événements pour chaque div
    divs.forEach((div) => {
        div.addEventListener('click', (event) => {
            event.preventDefault(); // Empêchez l'ouverture du lien <a>
            const key = div.getAttribute('data-color'); // récupérer le data-color (la clef pour CGS_COLORS)
            changeColor(CGS_COLORS[key]); // Changer la couleur primary et stocker la sélection en session
            console.log('Couleur changée et stockée en session:', CGS_COLORS[key]);
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

// Fonction pour afficher une preview de certaines pages
function preview(PREVIEWS) {
    PREVIEWS.forEach(preview => {
        preview.addEventListener('click', function() {
            const box = preview.closest('li.list-item');
            const view = box.querySelector('div.list-preview');

            if (view) {
                view.classList.remove('cgs-hidden');
                view.addEventListener('click', function() {
                    view.classList.add('cgs-hidden');
                });
            }


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

        // Sélection du prochain élément cgs-hidden
        let next = swapable.nextElementSibling;
        while (next) {
            if (next.classList.contains('cgs-swap-visible')) {
                next.classList.remove('cgs-swap-visible');
                swapable.classList.add('cgs-open');
                break;
            } else if (next.classList.contains('cgs-swap-hidden')) {
                next.classList.remove('cgs-swap-hidden');
                swapable.classList.remove('cgs-open');
                hideSwapable(smooth, horizontal, next);
                break;
            }            
            next = next.nextElementSibling;
        }

        // console.log("SWAP: ", swapable, "NEXT: ", next);

        if (next) {
            swaper.addEventListener('click', function () {
                primaryIcon.classList.toggle('cgs-hidden');
                secondaryIcon.classList.toggle('cgs-hidden');
                swapable.classList.toggle('cgs-open');
                news = swapable.closest('cgs-news');
                if (news) {
                    news.classList.toggle('cgs-open');
                }
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
        } else {
            swaper.addEventListener('click', function () {    
                console.info("Pas de prochain élément à afficher");
            });
        }
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

// Gestion de la partie NEWS
function newsBlock(box) {
    const button = box.querySelector('div.news');
    const news = box.querySelectorAll('nav.news li');
    let highlight = false;
    for (const item of news) {
        // On vérifie si un des items contient une des classes du tableau HIGHLIGHTED
        if ([...item.classList].some(className => HIGHLIGHTED.includes(className))) {
            console.log(item);
            highlight = true
        }
    }        
    console.log("BUTTON", button, "NEWS", news);
    if (news && highlight) {
        button.classList.add('highlighted');
    }
}

// Gestion de la zone de recherche
function searchBlock(form) {

    ////////////////// INITIALISATION DES VARIABLES ////////////////////

    const urlParams = new URLSearchParams(window.location.search);
    const activeBox = document.querySelector('fieldset.active');

    const activeCategoryDiv = document.getElementById('activeCategory');    
    const categoryName = activeCategoryDiv.getAttribute('data-name');
    console.log("CategoryName : ", categoryName);
    const selectedCategory = urlParams.get(categoryName);
    const categoryButtons = document.querySelectorAll(`input[name="${categoryName}"]`);
    const categoryLabel = activeCategoryDiv.getAttribute('data-nom');

    const activeExtensionDiv = document.getElementById('activeExtension');
    const selectedExtension = urlParams.get('extension');
    const extensionButtons = document.querySelectorAll('input[name="extension"]');

    const selectedTags = urlParams.getAll('tag');
    const selectedQuery = urlParams.get('query');    
    const selectedDate = [urlParams.get('start_date'), urlParams.get('end_date')];    
    const tagButtons = document.querySelectorAll('.tag-button');

    const CGSFORM = document.getElementById('cgs-search-form');

    const activeTagsDiv = document.getElementById('activeTags');
    const activeQueryDiv = document.getElementById('activeQuery');
    const activeDateDiv = document.getElementById('activeDate');
    
    // const queryButton = document.querySelector('fieldset.recherche .filter_search');
    ///////////////////// ECOUTEURS D'EVENEMENTS ///////////////////////

    // Choix d'une catégorie
    if (categoryButtons) {
        categoryButtons.forEach(radio => {
            radio.addEventListener('change', function() {
                submitForm();
            });
        }); 
    }

    // Choix d'une extension 
    if (extensionButtons) {
        extensionButtons.forEach(radio => {
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
    // console.log("Category :", (selectedCategory), "Tags :", selectedTags, "Query :", selectedQuery, "Date :", selectedDate, "Extension :", selectedExtension);

    if (
        (selectedCategory && selectedCategory != "*") || 
        (selectedExtension && selectedExtension != "*") || 
        (selectedQuery && selectedQuery != "") || 
        selectedTags.length > 0 || 
        selectedDate[0] || 
        selectedDate[1]
    ) {
        // Afficher la catégorie active
        activeBox.style.display = 'flex';

        // Afficher la catégorie active
        if (selectedCategory) {
            // ajout d'un bouton cliquable (pour supprimer la catégorie en cours et sélectionner automatiquement "toutes")
            const onClickFunction = function() {
                categoryButtons.forEach(radio => {
                    radio.checked = false;                    
                });
                if (!selectedExtension) {
                    extensionButtons.forEach(radio => {
                        radio.checked = false;
                    });
                }
                submitForm();
            };
            addActive(activeCategoryDiv, categoryLabel, selectedCategory, onClickFunction);
        }

        // Afficher l'extension active
        if (selectedExtension) {
            const onClickFunction = function() {
                extensionButtons.forEach(radio => {
                    radio.checked = false;
                });
                if (!selectedCategory) {
                    categoryButtons.forEach(radio => {
                        radio.checked = false;
                    });
                }
                submitForm();
            };
            addActive(activeExtensionDiv, 'Fichier', selectedExtension.split('_')[0], onClickFunction);
        } 

        // Afficher la recherche active
        if (selectedQuery) {
            const onClickFunction = function() {
                const queryInput = document.querySelector('input[name="query"]');
                queryInput.value = '';
                submitForm();
            };
            addActive(activeQueryDiv, 'Recherche', selectedQuery, onClickFunction);
        }

        // Afficher les tags actifs
        if (selectedTags.length > 0) {
            // Afficher les tags actifs
            selectedTags.forEach(tagName => addTag(tagName));    
        }

        // Afficher la date de début
        if (selectedDate[0]) {
            const onClickFunction = function() {
                const startDateInput = document.querySelector('input[name="start_date"]');
                startDateInput.value = '';
                submitForm();
            }
            addActive(activeDateDiv, 'Début', selectedDate[0], onClickFunction);
        }

        // Afficher la date de fin
        if (selectedDate[1]) {
            const onClickFunction = function() {
                const endDateInput = document.querySelector('input[name="end_date"]');
                endDateInput.value = '';
                submitForm();
            };
            addActive(activeDateDiv, 'Fin', selectedDate[1], onClickFunction);
        }

    }
    
    /////////////////////// FONCTIONS DIVERSES /////////////////////////

    // Ajouter un élément actif
    function addActive(box, label, value, onClickFunction) {
        const div = document.createElement('div');        
        
        const p = document.createElement('p');
        p.classList.add('active-item');

        const spanKey = document.createElement('span');
        spanKey.classList.add('key');
        spanKey.textContent = label + ' : ';

        const spanField = document.createElement('span');
        spanField.classList.add('field');
        spanField.textContent = value;            
        
        const svg = document.querySelector('#cgs-close svg').cloneNode(true);
        svg.id = 'svg_close_categorie';
        svg.classList.add('cgs-mid-icon', 'cgs-close');
        svg.onclick = onClickFunction;
        
        p.appendChild(spanKey);
        p.appendChild(spanField);
        div.appendChild(p);
        div.appendChild(svg);
        box.appendChild(div);

        return div;
    }
    
    // Ajout d'un tag en utilisant les tags personnalisés
    function addTag(tagName) {
        if (![...activeTagsDiv.children].some(tagDisplay => tagDisplay.textContent.startsWith(tagName))) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'tag';
            input.value = tagName;
            CGSFORM.appendChild(input);
    
            // Fonction onClick personnalisée qui nécessite le div
            const onClickFunction = function() {
                CGSFORM.removeChild(input);
                activeTagsDiv.removeChild(div); // div doit être défini dans cette portée
                submitForm();
            };
    
            // Ajouter un élément actif et récupérer le div créé
            const div = addActive(activeTagsDiv, 'Tag', tagName, onClickFunction);
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

//////////////////////////////////////////   VARIABLES   //////////////////////////////////////////////////

const CGS_COLORS = {
    fonce: '#008770',
    cyan: '#00b3be',
    clair: '#92d400',
    gris: '#928b81'
};

const HIGHLIGHTED = ["convoc", "enquete", "amicale"]