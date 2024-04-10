document.addEventListener("DOMContentLoaded", function() {
    console.log("Page d'administration chargée");
    // On récupère le type de menu
    const bodyClass = document.body ? document.body.getAttribute('class') : '';
    console.log(bodyClass);

    // Page de menu
    if (bodyClass.includes('menu')) {
        cgsMenu();
    }

    // Page de visualisation des convocations et des comptes-rendus
    if (bodyClass.includes('doc')) {
        cgsDoc();
        const container = document.getElementById('viewer');
        if (container) {
            cgsViewer(container);
        }
    }
});

// Gestion du menu
function cgsMenu() {
    console.log("Menu chargé");
}

// Gestion de la copie des emails
function cgsList() {
    console.log("Liste chargée");
    
    // Container des boutons
    const sectionAction = document.getElementById("action-buttons");
    if (sectionAction) {
        actionButtons();
    }

    // Gestion des boutons d'actions
    function actionButtons() {
        const copy = document.getElementById("cgs-copy");
        const download = document.getElementById("cgs-download");
        const print = document.getElementById("cgs-print");

        if (copy) {
            copy.addEventListener("click", copyMails);
        }
    }
    
    // Copie des emails
    function copyMails() {
        const emailSpans = document.querySelectorAll("#emailsContainer .email");
        console.log(emailSpans);
        const emails = Array.from(emailSpans).map(span => span.textContent.trim());
        const emailText = emails.join(", ");
    
        navigator.clipboard.writeText(emailText).then(function() {
            console.log('Copie réussie');
        }, function(err) {
            console.error('Erreur lors de la copie', err);
        });
    }  
}

// Gestion des documents
function cgsDoc() {
    console.log("Document chargé");
}

// Gestion de la visualisation des documents
async function cgsViewer(container) {
    console.time("Temps de chargement du PDF");
    console.time("Temps de chargement total");

    const isSmartphone = isMobileDevice();
    console.log(isSmartphone ? 'Appareil mobile détecté' : 'Grand écran détecté');

    const url = container.getAttribute('data-url');
    if (!url) {
        console.error('URL du PDF non définie');
        return;
    }
    console.log('URL du PDF : ' + url);

    // Barre de progression
    const progressBox = document.querySelector('div.cgs-progress');
    const progressValue = progressBox.querySelector('p.progress-value');
    let progress = 0;
    updateProgress(progress);

    try {
        const pdf = await pdfjsLib.getDocument(url).promise;
        console.log('PDF chargé');
        console.timeEnd("Temps de chargement du PDF");

        const progressPage = 100 / pdf.numPages;

        // Chargez et affichez toutes les pages du PDF
        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            await renderPage(pdf, pageNum, progressPage, container);
        }
        console.log('Toutes les pages sont chargées');
        console.timeEnd("Temps de chargement total");
        progressBox.style.display = 'none';        
        viewerAction(pdf.numPages);

    } catch (reason) {
        console.error(reason);
    }

    async function renderPage(pdf, pageNum, progressPage, container) {
        const page = await pdf.getPage(pageNum);
        console.time(`Temps de chargement de la page ${pageNum}`);
        const scale = isSmartphone ? window.devicePixelRatio : Math.max(window.devicePixelRatio || 1, 3);
        const viewport = page.getViewport({scale: scale});
        let canvas = document.createElement('canvas');
        canvas.id = 'page-' + pageNum;
        container.appendChild(canvas);
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderContext = {
            canvasContext: canvas.getContext('2d'),
            viewport: viewport
        };

        await page.render(renderContext).promise;
        console.timeEnd(`Temps de chargement de la page ${pageNum}`);
        progress += progressPage;
        updateProgress(progress);
    }

    function updateProgress(progress) {
        document.documentElement.style.setProperty('--progress', `${progress}%`);
        progressValue.textContent = `${Math.floor(progress)}%`;
    }

    // Gestion des actions de navigation
    function viewerAction(maxPage) {
        // On récupère le container de la barre d'actions
        const actionBox = document.querySelector('nav.viewer');
        actionBox.style.display = 'block';

        // On défini la valeur maximale de l'input de sélection de page
        const pageAction = actionBox.querySelector('input');
        pageAction.max = maxPage;

        // On affiche le nombre total de pages
        const maxPageBox = actionBox.querySelector('span.max-page');
        maxPageBox.textContent = maxPage;
        
        // On récupère tous les canvas ainsi que leur currentWidth
        const canvas = container.querySelectorAll('canvas');
        const initialWaidth = canvas[0].offsetWidth;
        let currentWidth = initialWaidth;

        // Boutons
        const firstAction = document.getElementById('first-page');
        const nextAction = document.getElementById('next-page');
        const lastAction = document.getElementById('last-page');
        const prevAction = document.getElementById('prev-page');
        const zoomIn = document.getElementById('zoom-in');
        const zoomOut = document.getElementById('zoom-out');
        const fullscreen = document.getElementById('fullscreen');

        // Elements divers
        const fsButton = fullscreen.querySelector('button');
        

        // Actions de page (première, précédente, suivante, dernière)
        firstAction.addEventListener('click', () => {
            if (currentPage != 1) {
                currentPage = 1;
                pageAction.value = currentPage;
                const scroll = scrollToPage(currentPage);
                console.log(scroll);
            }
        });
        prevAction.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                pageAction.value = currentPage;
                const scroll = scrollToPage(currentPage);
                console.log(scroll);
            }
        });        
        lastAction.addEventListener('click', () => {
            if (currentPage != maxPage) {
                currentPage = maxPage;
                pageAction.value = currentPage;
                const scroll = scrollToPage(currentPage);
                console.log(scroll);
            }
        });
        nextAction.addEventListener('click', () => {
            if (currentPage < maxPage) {
                currentPage++;
                pageAction.value = currentPage;
                const scroll = scrollToPage(currentPage);
                console.log(scroll);
            }
        });
        // Action de saisie de la page
        pageAction.addEventListener('change', () => {
            const requestedPage = parseInt(pageAction.value);
            if (!isNaN(requestedPage) && requestedPage >= 1 && requestedPage <= pageAction.max) {
                currentPage = requestedPage;
                const scroll = scrollToPage(currentPage);
                console.log(scroll);
            } else {
                // Si la valeur entrée est hors des limites, réinitialiser à la valeur actuelle
                pageAction.value = currentPage;
            }
        });

        // ACTIONS DE ZOOM
        fullscreen.addEventListener('click', () => {
            if (fsButton.expanded) {
                fullScreen(false);
            } else {
                fullScreen(true);
            }            
        });
        zoomIn.addEventListener('click', () => {
            currentWidth *= 1.1;
            if (currentWidth > canvas[0].width) {
                currentWidth = canvas[0].width;
            }
            applyZoom(currentWidth);
        });
        zoomOut.addEventListener('click', () => {
            currentWidth *= 0.9;
            if (currentWidth < 350) {
                currentWidth = 350;
            }
            applyZoom(currentWidth);
        });

        function scrollToPage(pageNum) {
            const pageElement = document.getElementById(`page-${pageNum}`);
            if (pageElement) {
                const beforeScrollTop = container.scrollTop;
                const elementTopRelativeToContainer = pageElement.offsetTop - container.offsetTop;
                
                pageElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
                // Cette ligne est juste indicative pour comprendre le calcul
                console.log('Position attendue après défilement : ' + elementTopRelativeToContainer);
                
                return elementTopRelativeToContainer;
            }
        }

        function fullScreen(bool) {
            const expand = fsButton.querySelector('.expand');
            const compress = fsButton.querySelector('.compress');

            // On met à jour l'attribut expanded du bouton
            fsButton.expanded = bool;

            if (bool) {// On entre en mode plein écran                
                container.style.setProperty('--canvas-max-width', '100%');
                container.style.setProperty('--canvas-max-height', 'none');
                container.style.setProperty('--canvas-width', 'initial');
                container.style.justifyContent = 'center';
                currentWidth = initialWaidth;
                expand.classList.add('cgs-hidden');
                compress.classList.remove('cgs-hidden');
                fsButton.setAttribute('title', 'Quitter le mode plein écran');
                fsButton.setAttribute('alt', 'Quitter le mode plein écran');
            } else {// On quitte le mode plein écran
                container.style.setProperty('--canvas-max-width', '100%');
                container.style.setProperty('--canvas-max-height', 'calc(100vh - (var(--header-height) + var(--footer-height) + var(--header-padding)))');
                container.style.setProperty('--canvas-width', 'initial');
                container.style.justifyContent = 'center';
                currentWidth = initialWaidth;
                expand.classList.remove('cgs-hidden');
                compress.classList.add('cgs-hidden');
                fsButton.setAttribute('title', 'Passer en mode plein écran');
                fsButton.setAttribute('alt', 'Passer en mode plein écran');
            }
        }

        function applyZoom() {
            console.log('currentWidth : ' + currentWidth);
            console.log('container width : ' + container.offsetWidth);
            if (currentWidth > container.offsetWidth) {
                container.style.justifyContent = 'flex-start';
                container.style.overflowX = 'scroll';                
            } else {
                container.style.justifyContent = 'center';
                container.style.overflowX = 'initial';                
            }
            container.style.setProperty('--canvas-width', `${currentWidth}px`);
            container.style.setProperty('--canvas-max-height', 'none');
            container.style.setProperty('--canvas-max-width', 'none');
        }
    }    
}

function isMobileDevice() {
    return /Mobi/i.test(navigator.userAgent);
}