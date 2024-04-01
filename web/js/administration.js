document.addEventListener("DOMContentLoaded", function() {
    console.log("Page d'administration chargée");
    // On récupère le type de menu
    const bodyClass = document.body ? document.body.getAttribute('class') : '';
    console.log(bodyClass);

    // Page de menu
    if (bodyClass.includes('menu')) {
        cgsMenu();
    }

    // Page de listing et de recherche des convocations et des comptes-rendus
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

    // Gestion de la courbure du formulaire de recherche
    const recherche = document.getElementById('searchColumn');
    if (recherche) {
        const resizeObserver = new ResizeObserver(VerticalWave);
        resizeObserver.observe(recherche);        
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
    
    // Mise en forme de la vague du formulaire de recherche
    function VerticalWave() {
        const width = recherche.offsetWidth;
        const height = recherche.offsetHeight;

        const Yscale = 1.1 / (160 / width);
        const Xscale = 1 / (800 / height);

        document.documentElement.style.setProperty('--courbure-scaling-x', Xscale);
        document.documentElement.style.setProperty('--courbure-scaling-y', Yscale);        
    }
}

// Gestion des documents
function cgsDoc() {
    console.log("Document chargé");
}

// Gestion de la visualisation des documents
function cgsViewer(container) {    
    const url = container.getAttribute('data-url');
    if (!url) {
        console.error('URL du PDF non définie');
        return;
    }
    console.log('URL du PDF : ' + url);

    // Initialiser la barre de progression
    const progressBox = document.querySelector('div.cgs-progress');
    const progressValue = progressBox.querySelector('p.progress-value');

    // on set --progress à 0
    let progress = 0;
    updateProgress(progress);

    // Charger le document PDF
    pdfjsLib.getDocument(url).promise.then(pdf => {
        console.log('PDF chargé');

        // Valeur d'une page en %
        const progressPage = 100 / pdf.numPages;

        let lastRenderedPagePromise = Promise.resolve(); // Promesse pour chaîner les rendus

        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            // Créez un élément canvas pour chaque page dans l'ordre
            let canvas = document.createElement('canvas');
            canvas.id = 'page-' + pageNum;
            container.appendChild(canvas);

            // Chaîner le rendu des pages pour maintenir l'ordre
            lastRenderedPagePromise = lastRenderedPagePromise.then(() => {
                return pdf.getPage(pageNum).then(page => {
                    console.log('Page ' + pageNum + ' chargée');
                    const viewport = page.getViewport({scale: 1});
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
    
                    const renderContext = {
                        canvasContext: canvas.getContext('2d'),
                        viewport: viewport
                    };
                    return page.render(renderContext).promise.then(() => {
                        console.log('Page ' + pageNum + ' rendue');
                        progress += progressPage; 
                        console.log('Progression : ' + progress);
                        updateProgress(progress);
                        if(pageNum === pdf.numPages) {
                            console.log('Progression terminée');
                            progressBox.style.display = 'none';
                        }
                    });
                });
            });
        }
    }, reason => {
        console.error(reason);
    });

    function updateProgress(progress) {
        document.documentElement.style.setProperty('--progress', `${progress}%`);
        progressValue.textContent = `${Math.floor(progress)}%`;
    }
}
