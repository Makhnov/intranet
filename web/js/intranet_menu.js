window.addEventListener('load', () => {
    // Fichier menu standard chargé
    console.log("Fichier menu.js chargé");

    // On vérifie si on est sur la page index de la FAQ ou des commissions
    const menuBox = document.querySelector('body.menu.cgs-faq ul.menu-box, body.menu.cgs-commissions ul.menu-box'); //, body.menu.cgs-amicale ul.menu-box

    if (menuBox) {
        const items = menuBox.querySelectorAll('li');
        adjustGridItems(items);
        window.addEventListener('resize', debounce(() => adjustGridItems(items), 250));
    }

    function adjustGridItems(items) {            

        // Réinitialiser les styles pour tous les éléments
        items.forEach(item => {
            item.style.gridColumnStart = '';
            item.style.transform = '';
        });
        
        // 1. Nombre de colonnes
        const columnWidth = getMenuItemSize();
        const menuBoxWidth = menuBox.clientWidth;
        const columns = Math.floor(menuBoxWidth / columnWidth);

        // 2. Nombre total d'items
        const itemCount = items.length;
    
        // 3. Reste de la division
        const remainder = itemCount % columns;
        const decal = columns - remainder;
    
        // console.log(`${columns} colonnes`);
        // console.log(`${itemCount} items`);
        // console.log(`Reste de ${itemCount}/${columns} = ${remainder}`);
        // console.log(`Decal = ${decal}`);
    
        // 4. Modification du grid-column pour les derniers éléments
        if (remainder > 0) {
            let startColumn;
            if (decal % 2 === 0) {
                // Si décalage est pair
                startColumn = decal / 2;
                for (let i = itemCount - remainder; i < itemCount; i++) {
                    items[i].style.gridColumnStart = `${startColumn + (i - (itemCount - remainder)) + 1}`;
                }
            } else {
                // Si décalage est impair
                startColumn = Math.ceil(decal / 2);
                for (let i = itemCount - remainder; i < itemCount; i++) {
                    items[i].style.gridColumnStart = `${startColumn + (i - (itemCount - remainder))}`;
                    // Translation de columnWidth / 2 vers la droite
                    items[i].style.transform = `translateX(${columnWidth / 2}px)`;
                }
            }
        }
    }

    // Variable itemSize
    function getMenuItemSize() {
        // Récupérer le style calculé de l'élément :root
        const style = window.getComputedStyle(document.documentElement);
        const itemSize = parseFloat(style.getPropertyValue('--menu-item-size'));
        const em = parseFloat(style.getPropertyValue('font-size'));
        // console.log(`--menu-item-size vaut actuellement : ${itemSize}em`);
        
        return itemSize * 3 * em;
    }
        
    // Debouncing
    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this, args = arguments;
            const later = function() {
                timeout = null;
                func.apply(context, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});