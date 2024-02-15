// Gestion du comportement des sous-menus pour les menus déroulants
document.addEventListener('DOMContentLoaded', function () {
    // Fichier barre de navigation chargé
    console.log("Fichier intranet.js chargé");
    
    // On récupère les ROOT
    const STYLE = getComputedStyle(document.body);
    
    // Sélectionnez toutes les divs avec la classe .logo-pochoir.right
    const pochoirDivs = document.querySelectorAll('.logo-pochoir.right');

    // Définissez les couleurs pour chaque pochoir
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

    // Ajoutez un gestionnaire d'événements pour chaque div
    pochoirDivs.forEach((div, index) => {
        div.addEventListener('click', (event) => {
            // Empêchez l'ouverture du lien <a>
            event.preventDefault();

            // Changez la couleur primary et stockez la sélection
            changeColor(pochoirColors[index]);
        });
    });
    
    // Ajout de la classe cgs-open lors du click sur le profil (si l'utilisateur est connecté)
    const profile = document.querySelector('ul.profile > .avatar');
    if (profile) {
        profile.addEventListener('click', function (event) {
            profile.closest('ul').classList.toggle('cgs-open');
        });
    }

    // Images en plein écran
    document.querySelectorAll('.cgs-expandable').forEach(img => {
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
    
    // SWAP
    const swapables = document.querySelectorAll('.cgs-swap');

    function hideSwapable(smooth=false, direction=false, element) {
        if (smooth) {
            if (direction) {        
                console.log('cgs-width-none')        
                element.classList.toggle('cgs-width-none');
            } else {
                console.log('cgs-height-none');
                element.classList.toggle('cgs-height-none');
            }
        } else {
            console.log('cgs-hidden');
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

    // scrolling < et > du footer
    const footerBox = document.querySelector('footer nav.footer ul.nav-box');
    const footerLeft = document.querySelector('footer nav.footer div.cgs-box.left');
    const footerRight = document.querySelector('footer nav.footer div.cgs-box.right');
    const footerIconMargin = parseFloat(STYLE.getPropertyValue('--nav-icon-margin'));
    const footerIconwidth = parseFloat(STYLE.getPropertyValue('--nav-icon-size'));
    const scrollAmount = 32 * (1.5 * footerIconMargin + footerIconwidth);

    if (footerBox) {
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

    // Agrandissement de la barre de recherche
    const searchButtons = document.querySelectorAll('cgs-search > svg, cgs-search > img');

    if (searchButtons.length === 3) {
        const searchBase = searchButtons[0];
        const searchOut = searchButtons[1];
        const searchIn = searchButtons[2];
    
        const searchBar = document.querySelector('cgs-search > form > input');
    
        searchBase.addEventListener('click', () => {
            searchBase.classList.add('cgs-hidden');
            searchOut.classList.remove('cgs-hidden');
            searchBar.classList.add('cgs-open');
        });
        searchOut.addEventListener('click', () => {
            searchOut.classList.add('cgs-hidden');
            searchIn.classList.remove('cgs-hidden');
            searchBar.classList.remove('cgs-open');
        });
        searchIn.addEventListener('click', () => {
            searchIn.classList.add('cgs-hidden');
            searchOut.classList.remove('cgs-hidden');
            searchBar.classList.add('cgs-open');
        });
        searchBar.addEventListener('focus', () => {
            searchBar.classList.add('cgs-open');
            searchBase.classList.add('cgs-hidden');
            searchIn.classList.add('cgs-hidden');
            searchOut.classList.remove('cgs-hidden');
        });
    }
});
