document.addEventListener('DOMContentLoaded', function () {

    // Fichier barre de navigation chargé
    console.log("Fichier quickbar.js chargé");

    // On récupère la barre rapide et la division qui contient la navigation contextuelle
    const quickbar = document.querySelector('cgs-quickbar');
    const contenu = document.querySelector('div.cgs-quickbar-content');

    // On vérifie le contenu de la barre rapide
    if (contenu.children.length !== 0) {
        // On supprime l'élément "contenu"
        quickbar.classList.remove('cgs-hidden');
    }
});