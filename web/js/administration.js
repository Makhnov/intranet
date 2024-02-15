document.addEventListener("DOMContentLoaded", function() {
    console.log("Page d'administration chargée");

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
});
