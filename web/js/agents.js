document.addEventListener('DOMContentLoaded', function() {
    console.log("Fichier agents.js chargé");

    const bodyClass = document.body.classList;

    if (bodyClass.contains('item')) {
        console.log("Item chargé")
        cgsItem();
    }
});

function cgsItem() {
    const choiceContainer = document.querySelectorAll('div.cgs-choice-container:not(.reduced)');
    const choiceContainerReduced = document.querySelectorAll('div.cgs-choice-container.reduced');

    choiceContainer.forEach((block) => manageChoiceBlock(block));
    choiceContainerReduced.forEach((block) => manageChoiceBlockReduced(block));

    function manageChoiceBlock(block) {
        const optionsBlock = block.querySelector("ul.choice-list");
        const contentBlock = block.querySelector("div.cgs-choice-content");

        // console.log("not reduced", block);
        const options = optionsBlock.querySelectorAll("ul.choice-list li");
        // console.log(options);
        const content = contentBlock.querySelectorAll("div.cgs-choice-content > div");
        // console.log(content);

        // Ajout de l'écouteur d'événement sur les liens
        options.forEach(option => {
            option.addEventListener('click', function() {
                if (!this.classList.contains('cgs-selected')) {
                    options.forEach(l => l.classList.remove('cgs-selected'));
                    this.classList.add('cgs-selected');
                    const targetId = this.getAttribute('data-target');

                    content.forEach(block => {
                        if (block.id === targetId) {
                            block.classList.remove('cgs-hidden');
                        } else {
                            block.classList.add('cgs-hidden');
                        }
                    });
                }
            });
        });

        // Créer un nouvel observateur de redimensionnement
        const resizeObserver = new ResizeObserver(entries => {
            for (let entry of entries) {
                const {width} = entry.contentRect;
                // on récupère le padding (variable root : --padding-choice)
                const padding = getComputedStyle(contentBlock).getPropertyValue('--padding-choice');
                // console.log(`La nouvelle largeur des options est : ${width}`);
                contentBlock.style.width = `calc(${width - 2}px - ${padding} * 2)`;
            }
        });
    
        // Commencer à observer l'élément options
        resizeObserver.observe(optionsBlock);
    }
    
    function manageChoiceBlockReduced(block) {        
        console.log("reduced", block);
        const optionsBlockReduced = block.querySelector("ul.choice-list");
        const contentBlockReduced = block.querySelector("div.cgs-choice-content");

        console.log("Reduced", block);
        const reducedOptions = optionsBlockReduced.querySelectorAll("ul.choice-list li");
        console.log(reducedOptions);
        const reducedContent = contentBlockReduced.querySelectorAll("div.cgs-choice-content > div");
        console.log(reducedContent);

        // Ajout de l'écouteur d'événement sur les liens
        reducedOptions.forEach(option => {
            option.addEventListener('click', function() {
                if (!this.classList.contains('cgs-selected')) {
                    reducedOptions.forEach(l => l.classList.remove('cgs-selected'));
                    this.classList.add('cgs-selected');
                    const targetId = this.getAttribute('data-target');

                    reducedContent.forEach(block => {
                        if (block.id === targetId) {
                            block.classList.remove('cgs-hidden');
                        } else {
                            block.classList.add('cgs-hidden');
                        }
                    });
                }
            });
        });    
    }
}