document.addEventListener('DOMContentLoaded', function () {
    console.log("Fichier stremfield.js chargé");

    // On vérifie la présence d'un tableau dans le document
    const TABLEBOXES = document.querySelectorAll('div.cgs-block-table');
    if (TABLEBOXES.length > 0) {
        TABLEBOXES.forEach(box => {
            getTableData(box);
        });
    }
});


// Récupération des valeurs des attributs data-row et data-column
function getTableData(box) { 
    const tableaux = box.querySelectorAll('table');
    const containerWidth = box.offsetWidth;
    // console.log(containerWidth);

    if (tableaux) {
        for (let i = 0; i < tableaux.length; i++) {
            merge_cells(tableaux[i]);
        }           
    }

    function merge_cells(tab) {
        // console.log(tab);
        const mergeRaw = tab.getAttribute('data-merge');            
        if (mergeRaw) {
            const merge = JSON.parse(mergeRaw.replace(/'/g, '"'));
            merge.forEach(m => {
                const col = m['col'];
                const row = m['row'];
                const colspan = m['colspan'] || 1;
                const rowspan = m['rowspan'] || 1;
                const cell = tab.rows[row].cells[col];
                cell.colSpan = colspan;
                cell.rowSpan = rowspan;
    
                // Vérifier si la cellule touche le bord droit du tableau
                if ((col + colspan) === tab.rows[row].cells.length) {
                    cell.style.borderRight = "2px solid var(--vert)";
                }

    
                // Vérifier si la cellule touche le fond du tableau
                if ((row + rowspan) === tab.rows.length) {
                    cell.style.borderBottom = "2px solid var(--vert)";
                }     
                
                // Vérifier si on a un rowspan pour ajuster la cellule de la dernière ligne concernée par ce rowspan
                if (rowspan > 1) {
                // Calculer l'indice de la dernière ligne affectée par le rowspan
                const lastRowAffected = row + rowspan - 1;

                // S'assurer que cette dernière ligne existe dans le tableau
                if (lastRowAffected < tab.rows.length) {
                    // Trouver la cellule à gauche de la cellule fusionnée sur la dernière ligne affectée
                    // Il faut s'assurer que 'col - 1' est valide (c'est-à-dire qu'il y a une cellule à gauche)
                    if (col > 0 && tab.rows[lastRowAffected].cells[col - 1]) {
                        // Ajouter la classe "cgs-not-last" à cette cellule
                        tab.rows[lastRowAffected].cells[col - 1].classList.add("cgs-not-last");
                    }
                }
            }
            });
            empty_cells(tab, true);
        } else {
            empty_cells(tab, false);
        }
    }      

    function empty_cells(tab, merge) {
        let emptyCells = 0;
        for (let i = 0; i < tab.rows.length; i++) {
            for (let j = 0; j < tab.rows[i].cells.length; j++) {
                // console.log('row:', i, 'col', j)
                if (tab.rows[i].cells[j].innerHTML === "None") {
                    // console.log("Cellule vide")
                    tab.rows[i].cells[j].innerHTML = "";
                    if (merge) {
                        emptyCells++;
                    }                   
                }
            }
            if (emptyCells > 0) {
                // console.log("ON SUPPRIME LES DERNIERES CELLULES")
                // on supprime les X dernieres cellules.
                for (let k = 0; k < emptyCells; k++) {
                    tab.rows[i].deleteCell(-1);
                }
                emptyCells = 0;
            }
        }
    }
}