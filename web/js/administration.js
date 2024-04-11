
document.addEventListener("DOMContentLoaded", function() {
    console.log("Page d'administration chargée");
    // On récupère le type de menu
    const bodyClass = document.body ? document.body.getAttribute('class') : '';

    // Page de menu
    if (bodyClass.includes('menu')) {
        cgsMenu();
    }

    if (bodyClass.includes('list')) {
        cgsList();
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

// Affichage des documents PDF
function cgsViewer(container) {
    console.time("Chargement du PDF");
    console.time("Préchargement");
    console.time("Chargement initial");
    const smartphone = isMobileDevice();
    console.log(smartphone ? 'Appareil mobile détecté' : 'Grand écran détecté');

    let progress = 1;
    let preloadedPages = {};
    let pagesInRendering = 0;
    let pagesRendered = 0;
    let currentPage = 1;
    let maxPages = 1;

    // Observer pour les éléments entrant et sortant du viewport
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            const pageNum = parseInt(entry.target.getAttribute('data-page'));
            if (entry.isIntersecting && !preloadedPages[pageNum]?.rendered) {
                renderPage(pageNum);
                preloadedPages[pageNum].rendered = true;
            }
        });
    }, {root: container, threshold: 0.1});

    const spinner = document.getElementById('spinner_svg');
    const progressValue = document.querySelector('div.cgs-progress p.progress-value');
    
    baseViewer(container);

    // Gestion de la visualisation des documents
    async function baseViewer(container) {
        const url = container.getAttribute('data-url');
        if (!url) {
            console.error('URL du PDF non définie');
            return;
        }
        console.log('URL du PDF : ' + url);

        try {
            const pdf = await pdfjsLib.getDocument(url).promise;
            maxPages = pdf.numPages;
            console.timeEnd("Chargement du PDF");

            // Préchargez les pages sans les rendre
            for (let pageNum = 1; pageNum <= maxPages; pageNum++) {
                await preloadPage(pdf, pageNum, container);                
            }

            viewerAction(maxPages);
            console.timeEnd("Préchargement");


        } catch (reason) {
            console.error(reason);
        }
    }
    
    // Préchargement des pages
    async function preloadPage(pdf, pageNum, container) {
        const page = await pdf.getPage(pageNum);
        const scale = smartphone ? window.devicePixelRatio : Math.max(window.devicePixelRatio || 1, 3);
        const viewport = page.getViewport({ scale: scale });
    
        // Création d'un emplacement visuel pour la page
        const div = document.createElement('div');
        div.classList.add('cgs-page');
        div.setAttribute('data-page', pageNum);
        div.setAttribute('id', `block-${pageNum}`);
        div.classList.add('cgs-placeholder');

        // Création d'un élément canvas pour le rendu de la page
        let placeholder = document.createElement('canvas');
        placeholder.width = viewport.width;
        placeholder.height = viewport.height;
        placeholder.setAttribute('id', `page-${pageNum}`);
        div.appendChild(placeholder);

        // Ajout du spinner de chargement
        div.appendChild(spinner.cloneNode(true));

        // On ajoute l'élément dans le viewer et on l'observe
        container.appendChild(div);
        observer.observe(div);

        preloadedPages[pageNum] = { page, viewport, placeholder, rendered: false };
    }

    // Fonction pour rendre une page unique basée sur les données préchargées
    async function renderPage(pageNum) {
        console.time(`Rendu de la page ${pageNum}`);
        if (!preloadedPages[pageNum] || preloadedPages[pageNum].rendering) return;
    
        pagesInRendering += 1; // Commencer le rendu d'une page
        preloadedPages[pageNum].rendering = true; // Marquez le début du rendu
        
        const { page, viewport, placeholder } = preloadedPages[pageNum];
        let context = placeholder.getContext('2d');
        let renderContext = {
            canvasContext: context,
            viewport: viewport
        };
    
        try {
            await page.render(renderContext).promise;
            placeholder.closest('div').classList.remove('cgs-placeholder');
            preloadedPages[pageNum].rendered = true;
            console.log(`Page ${pageNum} rendue`);
            pagesRendered += 1; // Une page de plus est rendue
        } catch (error) {
            console.error(`Erreur lors du rendu de la page ${pageNum}:`, error);
        } finally {
            pagesInRendering -= 1; // Fin du rendu d'une page
            preloadedPages[pageNum].rendering = false;
            updateProgress(); // Mise à jour de la barre de progression
        }

        console.timeEnd(`Rendu de la page ${pageNum}`);
    }

    // Mise à jour de la barre de progression
    function updateProgress() {
        let total = Object.keys(preloadedPages).length;
        let progress = (pagesRendered / total) * 100;
        document.documentElement.style.setProperty('--progress', `${progress}%`);
        progressValue.textContent = `${Math.round(progress)}%`;
    }

    // Actions de navigation
    function viewerAction(maxPages) {
        // On récupère le container de la barre d'actions
        const actionBox = document.querySelector('nav.viewer');
        if (!actionBox) {
            console.error('Container de navigation non trouvé');
            return;
        }

        // On défini la valeur maximale de l'input de sélection de page
        const pageAction = actionBox.querySelector('input');
        pageAction.max = maxPages;

        // On affiche le nombre total de pages
        const maxPagesBox = actionBox.querySelector('span.max-page');
        maxPagesBox.textContent = maxPages;
        
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
            if (currentPage != maxPages) {
                currentPage = maxPages;
                pageAction.value = currentPage;
                const scroll = scrollToPage(currentPage);
                console.log(scroll);
            }
        });
        nextAction.addEventListener('click', () => {
            if (currentPage < maxPages) {
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

    // Type d'appaareil utilisé
    function isMobileDevice() {
        return /Mobi/i.test(navigator.userAgent);
    }
}