document.addEventListener("DOMContentLoaded", function() {
    console.log("Page d'administration chargée");

    // Gestion de l'affichage des contenus des menus déroulants
    document.querySelectorAll('.accordion-title').forEach(function(title) {
        title.addEventListener('click', function() {
            // Trouver le contenu de l'accordéon associé
            const content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    });

    // Gestion de la copie des emails
    document.getElementById("cgs-copy").addEventListener('click', copyEmailsToClipboard);

    function copyEmailsToClipboard() {
        const emailText = document.getElementById("emailsToCopy").textContent;
        navigator.clipboard.writeText(emailText).then(function() {
            console.log('Copie réussie');
        }, function(err) {
            console.error('Erreur lors de la copie', err);
        });
    }

    // Gestion de la courbure du formulaire de recherche
    const recherche = document.getElementById('searchColumn');

    if (recherche != null) {
        //on lance un listener sur la taille du container 
        const resizeObserver = new ResizeObserver(VerticalWave);
        resizeObserver.observe(recherche);        
    }

    function VerticalWave() {
        const width = recherche.offsetWidth;
        const height = recherche.offsetHeight;

        const Yscale = 1.1 / (160 / width);
        const Xscale = 1 / (800 / height);

        document.documentElement.style.setProperty('--courbure-scaling-x', Xscale);
        document.documentElement.style.setProperty('--courbure-scaling-y', Yscale);        
    }
});
