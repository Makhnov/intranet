document.addEventListener('DOMContentLoaded', function() {
    console.log("Fichier mailing.js chargé");

    // Choix de la section par l'utilisateur (amicale ou convocation)
    const objects = document.getElementById('objects');
    if (objects) {
        listenObjectsChange(objects);
    }

    // On récupère le formulaire
    const form = document.querySelectorAll('form.cgs-mailing');
    if (form.length > 0) {
        displayForm();
    }
});

function listenObjectsChange(obj) {// Choix de la campagne par l'utilisateur (divers ou convocation)

    const convocation = document.getElementById('object_convocation');
    const amicale = document.getElementById('object_divers');

    const left = document.querySelector('section.left');
    const right = document.querySelector('section.right');
    const labelLeft = document.querySelector('label[for=object_divers]');
    const labelRight = document.querySelector('label[for=object_convocation]');
    const spanLeft = document.querySelector('span[for=object_divers]');
    const spanRight = document.querySelector('span[for=object_convocation]');

    obj.addEventListener('change', function(event) {
        if (event.target.type === 'radio') {
            radioObjectChange(event.target.value);
        }
    });
    spanLeft.addEventListener('click', function() {
        amicale.checked = true;
        radioObjectChange('divers');
    });
    spanRight.addEventListener('click', function() {
        convocation.checked = true;
        radioObjectChange('convocation');
    });


    if (convocation.checked) {
        radioObjectChange('convocation');
    } else if (amicale.checked) {
        radioObjectChange('divers');
    } else {
        radioObjectChange('none');
    }
    
    function radioObjectChange(value){
        if (value === 'divers') {
            left.classList.remove('cgs-pathed');
            labelLeft.style.display = 'flex';
            spanLeft.style.transform = 'scaleX(0)';
            right.classList.add('cgs-pathed');
            labelRight.style.display = 'none';
            spanRight.style.transform = 'scaleX(1)';
        } else if (value === 'convocation') {
            left.classList.add('cgs-pathed');
            labelLeft.style.display = 'none';
            spanLeft.style.transform = 'scaleX(1)';
            right.classList.remove('cgs-pathed');
            labelRight.style.display = 'flex';
            spanRight.style.transform = 'scaleX(0)';
        } else if (value === 'none') {
            left.classList.add('cgs-pathed');
            labelLeft.style.display = 'none';
            spanLeft.style.transform = 'scaleX(1)';
            right.classList.add('cgs-pathed');
            labelRight.style.display = 'none';
            spanRight.style.transform = 'scaleX(1)';
        } else {
            left.classList.add('cgs-pathed');
            labelLeft.style.display = 'none';
            spanLeft.style.transform = 'scaleX(1)';
            right.classList.add('cgs-pathed');
            labelRight.style.display = 'none';
            spanRight.style.transform = 'scaleX(1)';
        }
    }
}

function displayForm() {// Affichage des champs du formulaire en fonction des sélections utilisateurs

    // On récupère tous les selects et tous les radios.
    const selects = document.querySelectorAll('div.cgs-form-group[data-type=select]');
    const radios = document.querySelectorAll('input[type=radio][name=left_pages], input[type=radio][name=right_pages], input[type=radio][name=commissions]');
    
    // On récupère le bloc commissions
    const commissionsPages = document.querySelector('div.cgs-form-group[data-type=radio][data-id=commissions]');

    // On masque tous les champs qui doivent l'être au chargement de la page.
    initFields();

    // On écoute les changements sur les radios
    radios.forEach(radio => {
        radio.addEventListener('change', function(event) {
            if (event.target.type === 'radio') {
                const section = event.target.closest('.cgs-form-group ');
                const value = event.target.value;
                formRadioChange(section, value);
            }
        });
    });

    function formRadioChange(section=null, value=null) {
        if (section) {
            // On récupère la value actuelle du selected de la section (data-selected)
            let selected = section.getAttribute('data-selected');
            let valueType = 'select';
            let selectedType = 'select';

            if (value === "commissions") {
                valueType = 'radio';
                let showValue = commissionsPages.getAttribute('data-selected');
                let showCommission = document.querySelector(`div.cgs-form-group[data-type="select"][data-id="${showValue}"]`);
                if (showCommission) {
                    showCommission.classList.remove('cgs-hidden');
                }
            }

            if (selected === "commissions") {
                selectedType = 'radio';
                let hideValue = commissionsPages.getAttribute('data-selected');
                commissionsPages.setAttribute('data-selected', '');
                let unCheck = commissionsPages.querySelector(`input[type=radio][name=commissions][value="${hideValue}"]`);
                if (unCheck) {
                    unCheck.checked = false;
                }
                let hideCommission = document.querySelector(`div.cgs-form-group[data-type="select"][data-id="${hideValue}"]`);
                if (hideCommission) {
                    hideCommission.classList.add('cgs-hidden');
                    let unSelect = hideCommission.querySelector('select');
                    if (unSelect) {
                        unSelect.selectedIndex = 0;
                    }
                }
            }

            const showSelect = document.querySelector(`div.cgs-form-group[data-type="${valueType}"][data-id="${value}"]`);
            const hideSelect = document.querySelector(`div.cgs-form-group[data-type="${selectedType}"][data-id="${selected}"]`);

            if (showSelect) {
                showSelect.classList.remove('cgs-hidden');               
            }
            if (hideSelect) {
                hideSelect.classList.add('cgs-hidden');
            }

            section.setAttribute('data-selected', value);
            
        } else {
            console.log('pas de section');
        }        
    }

    function initFields() {
        selects.forEach(select => {
            select.classList.add('cgs-hidden');
        });
        commissionsPages.classList.add('cgs-hidden');

        let selected = [];

        radios.forEach(radio => {
            if (radio.checked) {
                const section = radio.closest('.cgs-form-group');
                section.setAttribute('data-selected', radio.value);
                selected.push(section);
            }
        });                

        selected.forEach(section => {
            const value = section.getAttribute('data-selected');
            if (value === "commissions") {
                commissionsPages.classList.remove('cgs-hidden');
                const select = document.querySelector(`div.cgs-form-group[data-type=select][data-id='${commissionsPages.getAttribute('data-selected')}']`);
                if (select) {
                    select.classList.remove('cgs-hidden');
                }
            } else {
                const select = document.querySelector(`div.cgs-form-group[data-type=select][data-id=${value}]`);
                if (select && !select.getAttribute('data-id').includes('commission')) {
                    select.classList.remove('cgs-hidden');
                }
            }
        });
    }
}