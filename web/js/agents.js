document.addEventListener('DOMContentLoaded', function() {
    console.log("Fichier agents.js chargé");

    const urlParams = new URLSearchParams(window.location.search);    
    const selectedCategory = urlParams.get('category');
    const selectedTags = urlParams.getAll('tag');
    const selectedQuery = urlParams.get('query');

    if (selectedCategory || selectedTags.length > 0 || selectedQuery) {
        const categoryButtons = document.querySelectorAll('input[name="category"]');
        const tagButtons = document.querySelectorAll('.tag-button');
        const faqFilterForm = document.getElementById('faqFilterForm');
        const activeCategoryDiv = document.getElementById('activeCategory');
        const activeTagsDiv = document.getElementById('activeTags');
        const activeQueryDiv = document.getElementById('activeQuery');

        // console log de toutes les variables fixes : 
        console.log("selectedTags : ", selectedTags);
        console.log("selectedCategory : ", selectedCategory);
        console.log("selectedQuery : ", selectedQuery);    
    
        // Afficher la catégorie active
        if (selectedCategory) {
            // ajout d'un bouton cliquable (pour supprimer la catégorie en cours et sélectionner automatiquement "toutes")
            const div = document.createElement('div');        
            const svg = document.querySelector('#cgs-close svg').cloneNode(true);
            const span = document.createElement('span');
            svg.id = 'svg_close_categorie';
            svg.classList.add('cgs-small-icon');
            svg.onclick = function() {
                categoryButtons.forEach(radio => {
                    radio.checked = false;
                });
                submitForm();
            };
            span.textContent = `Catégorie : ${selectedCategory}`;
            div.appendChild(span);
            div.appendChild(svg);
            activeCategoryDiv.appendChild(div);
        } else {
            const div = document.createElement('div');
            const span = document.createElement('span');
            span.textContent = 'Catégorie : Toutes';
            div.appendChild(span);
            activeCategoryDiv.appendChild(div);
        }
    
        if (selectedQuery) {
            const div = document.createElement('div');
            const svg = document.querySelector('#cgs-close svg').cloneNode(true);
            const span = document.createElement('span');
        
            svg.id = 'svg_close_query';
            svg.classList.add('cgs-small-icon');
            svg.onclick = function() {
                const queryInput = document.querySelector('input[name="query"]');
                queryInput.value = '';
                submitForm();
            };
            span.textContent = `Recherche : ${selectedQuery}`;
            div.appendChild(span);
            div.appendChild(svg);
            activeQueryDiv.appendChild(div);
        }

        if (selectedTags.length > 0) {
            // Afficher les tags actifs
            selectedTags.forEach(tagName => addTag(tagName));    
        }

        // ECOUTEURS D'EVENEMENTS
        
        // Ajout d'un tag par les tags populaires
        tagButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tagName = this.getAttribute('data-tag');
                addTag(tagName);
                submitForm();
            });
        });
    
        // Choix d'une catégorie
        categoryButtons.forEach(radio => {
            radio.addEventListener('change', function() {
                submitForm();
            });
        });
        
        function addTag(tagName) {
            if (![...activeTagsDiv.children].some(tagDisplay => tagDisplay.textContent.startsWith(tagName))) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'tag';
                input.value = tagName;
                faqFilterForm.appendChild(input);
        
                // Créer un div pour le tag actif
                const div = document.createElement('div');
                div.className = 'active-tag-div'; // ajouter une classe pour le style si nécessaire
                
                // Créer un span pour le texte du tag
                const span = document.createElement('span');
                span.textContent = tagName;
        
                // Cloner et préparer le SVG pour le bouton de suppression
                const svg = document.querySelector('#cgs-close svg').cloneNode(true);
                svg.id = 'svg_close_' + tagName; // Assurez-vous que l'ID est unique
                svg.classList.add('cgs-small-icon');
                svg.onclick = function() {
                    faqFilterForm.removeChild(input); // Retirer l'input caché
                    activeTagsDiv.removeChild(div); // Retirer le div du tag actif
                    submitForm(); // Resoumettre le formulaire pour mettre à jour les résultats
                };
        
                // Assembler le div du tag actif
                div.appendChild(span);
                div.appendChild(svg);
                activeTagsDiv.appendChild(div);
            }
        }
        
        function submitForm() {
            faqFilterForm.submit();
        }
    }
});
