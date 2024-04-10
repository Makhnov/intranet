// Gestion du comportement des sous-menus pour les menus déroulants
document.addEventListener('DOMContentLoaded', function () {
    // Fichier barre de navigation chargé
    console.log("Fichier compte_rendu.js chargé");

    // Récupération du bloc DOCX
    const DOCX = document.querySelectorAll('.cgs-block-docx');
    
    //Récupération d'un bouton chart
    const chartButtons = document.querySelectorAll('button.chartButton');
    const canvas = document.querySelectorAll('.block-chart_block > canvas');
    const img = document.querySelectorAll('.chartpng');
    if (chartButtons.length > 0) {
        console.log(canvas);
        console.log(chartButtons);
        for (let i = 0; i < chartButtons.length; i++) {
            chartButtons[i].addEventListener('click', function() {
                const id = canvas[i].id;
                const element = img[i];
                chartToPng(id, element);
            });
        }
    }
    
    if (DOCX.length > 0) {
        getTableData(DOCX);
    }
    
    // Récupération des valeurs des attributs data-row et data-column
    function getTableData(DOCX) {        
        const tableaux = document.querySelectorAll('.cgs-block-docx table'); 
        const containerWidth = DOCX[0].offsetWidth;
        // console.log(containerWidth);

        if (tableaux) {
            for (let i = 0; i < tableaux.length; i++) {
                col_width(tableaux[i]);
                merge_cells(tableaux[i]);
            }           
        }

        function col_width(tab) {
            const dataC = tab.getAttribute('data-cols');

            if (!dataC) {
                return;
            }
            
            const cols = parseInt(dataC, 10);
            const width = (100 / cols) + '%';
            tab.querySelectorAll('td').forEach(td => {
                td.style.minWidth = width;
                td.style.maxWidth = width;
            });
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
                        cell.style.borderRight = "2px solid black";
                    }

        
                    // Vérifier si la cellule touche le fond du tableau
                    if ((row + rowspan) === tab.rows.length) {
                        cell.style.borderBottom = "2px solid black";
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
    
    // CHART TO PNG
    function chartToPng(id, element) {
        const chartInstance = Chart.getChart(id); // Disponible dans Chart.js 3.x et plus récent
        
        if (chartInstance) {
            const url = chartInstance.toBase64Image();
            element.src = url; // Assurez-vous que c'est l'ID correct de votre balise <img>
        } else {
            alert("Instance de graphique non trouvée.");
        }
    }
});


