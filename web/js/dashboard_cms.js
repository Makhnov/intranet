document.addEventListener("DOMContentLoaded", function() {
    console.log("Page de gestion du CMS chargée");

    document.addEventListener('w-formset:ready', function (event) {
        console.info('ready', event);
        // On vérifie si le bloc contient un select avec une option numeric ou attachments
        // const select = event.target.querySelectorAll('select[id*="id_compte_rendu_documents"], select[id*="id_convocation_documents"]');
        // const numeric = event.target.querySelectorAll('select[id*="id_compte_rendu_documents"] option[value=numeric], select[id*="id_convocation_documents"] option[value=numeric]');
        // const attachments = event.target.querySelectorAll('select[id*="id_compte_rendu_documents"] option[value=attachments], select[id*="id_convocation_documents"] option[value=attachments]');
        // console.log(select, numeric, attachments);
        checkNumerics();
    });
    
    document.addEventListener('w-formset:added', function (event) {
        console.info('added', event);
        checkNumerics();
    });
    
    document.addEventListener('w-formset:removed', function (event) {
        console.info('removed', event);
        checkNumerics();
    });    
});

function checkNumerics() {
    console.log("CHECK NUMERICS");
    const selects = document.querySelectorAll('select[id*="id_compte_rendu_documents"], select[id*="id_convocation_documents"]');
    let numericCount = 0;
    selects.forEach(select => {
        select.removeEventListener('change', checkNumerics);
        select.addEventListener('change', checkNumerics);
        if (select.value === 'numeric') {
            numericCount++;
            console.log(numericCount);
            if (numericCount > 1) {
                const error = select.parentElement.parentElement.querySelector('div.w-field__errors');
                console.log(error);
                if (error) {
                    error.innerHTML = `
                        <svg class="icon icon-warning w-field__errors-icon" aria-hidden="true"><use href="#icon-warning"></use></svg>
                        <p class="error-message">C'est le ${numericCount}eme document en "Version numérique". Si vous souhaitez afficher une pièce-jointe choisissez l'option adéquate dans le menu déroulant ci-dessous.</p>
                    `;
                }
            }
        
        }
    });

    if (numericCount < 2) {
        selects.forEach(select => {            
            const error = select.parentElement.parentElement.querySelector('div.w-field__errors');
            console.log("Erreur", error);
            if (error) {
                error.innerHTML = '';
            }
        });
    }
}