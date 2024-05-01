document.addEventListener('DOMContentLoaded', function () {
    console.log("Fichier amicale.js chargé");

    try {
        // Initialisation de la carte
        const mapBox = document.getElementById('carte');
        const routeBox = document.getElementById('itineraire');
        const openInLink = document.getElementById('open-in-maps');

        if (!mapBox) throw new Error("Élément de carte introuvable.");
        const mapInfo = map(mapBox);
        itineraire(mapInfo.start, mapInfo.end, openInLink);

        const openRoute = document.querySelector('a.open-route');
        if (openRoute) {
            openRoute.addEventListener('click', function () {
                // Activation du contrôle de routage
                createRoute(mapInfo.map, mapInfo.start, mapInfo.end);
                // Lancement de la fonction positionBox
                positionBox();
            });
        } else {
            console.log("Élément 'a.open-route' non trouvé.");
        }

        observeRouting(mapBox, routeBox);

    } catch (error) {
        console.error("Erreur lors de l'initialisation de la carte ou des contrôles de routage:", error);
    }
});

function map(box) {
    console.log("Fonction map() appelée", box);
    // Initialisation des variables de coordonnées
    const urlParams = new URLSearchParams(window.location.search);
    let startLat = 43.08366, startLng = 0.947, startTxt = "Siège de la communauté de communes";
    if (urlParams.get('home') === 'true') {
        startLat = parseFloat(box.dataset.homeLat);
        startLng = parseFloat(box.dataset.homeLng);
        startTxt = "Chez moi !";
    }
    const endLat = parseFloat(box.dataset.endLat);
    const endLng = parseFloat(box.dataset.endLng);

    // Création de la carte
    const map = L.map(box).setView([startLat, startLng], 13);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

    // Ajout des marqueurs
    const departMarker = L.marker([startLat, startLng]).addTo(map).bindPopup(startTxt);
    const destinationMarker = L.marker([endLat, endLng]).addTo(map).bindPopup(`<b>${box.dataset.pointName}</b><br><a href="${box.dataset.pointLink}">Visitez le site</a>`);
    map.fitBounds(L.latLngBounds([startLat, startLng], [endLat, endLng]));

    // Customisation des icônes
    departMarker._icon.classList.add("map-depart");
    destinationMarker._icon.classList.add("map-destination");

    return { 'map': map, 'start': [startLat, startLng], 'end': [endLat, endLng] };
}

function observeRouting(mapBox, routeBox) {
    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node instanceof HTMLElement && (node.classList.contains('leaflet-routing-container') || node.classList.contains('leaflet-routing-error'))) {
                    // Le conteneur de routage a été ajouté à mapBox, maintenant déplacez-le dans routeBox
                    route(node, routeBox);
                }
            });
        });
    });

    // Surveillance des ajouts de nouveaux enfants à mapBox
    observer.observe(mapBox, { childList: true, subtree: true });
}


function route(box, container) {
    console.log("Fonction route() appelée");
    try {
        container.appendChild(box);
    } catch (error) {
        console.error("Erreur lors du déplacement du contrôle de routage:", error);
    }
}

function itineraire(start, end, link) {
    console.log("Fonction itineraire() appelée");
    try {
        if (!link) throw new Error("Conteneur des contrôles Leaflet introuvable.");
        link.href = `https://www.google.com/maps/dir/?api=1&origin=${start[0]},${start[1]}&destination=${end[0]},${end[1]}&travelmode=driving`;
    } catch (error) {
        console.error("Erreur lors de l'ajout du lien Google Maps:", error);
    }
}

function createRoute(map, start, end) {
    L.Routing.control({
        waypoints: [L.latLng(start[0], start[1]), L.latLng(end[0], end[1])],
        language: 'fr',
        routeWhileDragging: true
    }).addTo(map);
}

function positionBox() {
    const mapBox = document.getElementById('carte');
    const openInBox = document.getElementById('open-in-box');
    const sectionBox = document.querySelector('section.amicale.map');

    if (mapBox && openInBox) {

        const mapBoxRight = mapBox.offsetLeft + mapBox.offsetWidth;
        const sectionBoxWidth = sectionBox.offsetWidth;
        const rightPosition = sectionBoxWidth - mapBoxRight;

        // Appliquer la position calculée
        openInBox.style.right = `${rightPosition}px`;
        openInBox.style.zIndex = 999;

        console.log("Position right de openInBox ajustée à :", rightPosition);
    } else {
        console.log("Erreur : 'mapBox' ou 'openInBox' n'existe pas dans le DOM.");
    }
}