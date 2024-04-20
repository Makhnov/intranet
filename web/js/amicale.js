document.addEventListener('DOMContentLoaded', function () {
    console.log("Fichier amicale.js chargé");

    try {
        // Initialisation de la carte
        const mapBox = document.getElementById('carte');
        const openInLink = document.getElementById('open-in-maps');
        
        if (!mapBox) throw new Error("Élément de carte introuvable.");
        const mapInfo = map(mapBox);
        itineraire(mapInfo.start, mapInfo.end, openInLink);

    } catch (error) {
        console.info("Erreur lors de l'initialisation de la carte ou absence de carte:", error);
    }    
});

function map(box) {
    console.log("Fonction map() appelée");

    // Initialisation des variables de coordonnées
    const urlParams = new URLSearchParams(window.location.search);

    let startLat = 43.08366, startLng = 0.947, startTxt = "Siège de la communauté de communes";
    if (urlParams.get('home') === 'true') {
        if (box.dataset.homeLat && box.dataset.homeLng) {
            startLat = parseFloat(box.dataset.homeLat);
            startLng = parseFloat(box.dataset.homeLng);
            startTxt = "Chez moi !";
        }        
    }

    const endLat = parseFloat(box.dataset.endLat);
    const endLng = parseFloat(box.dataset.endLng);

    // Création de la carte
    const map = L.map(box).setView([startLat, startLng], 13);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19}).addTo(map);

    // Ajout des marqueurs
    const departMarker = L.marker([startLat, startLng]).addTo(map).bindPopup(startTxt);
    const destinationMarker = L.marker([endLat, endLng]).addTo(map).bindPopup(`<b>${box.dataset.pointName}</b><br><a href="${box.dataset.pointLink}">Visitez le site</a>`);
    map.fitBounds(L.latLngBounds([startLat, startLng], [endLat, endLng]), { padding: [75, 75] });

    // Customisation des icônes
    departMarker._icon.classList.add("map-depart");
    destinationMarker._icon.classList.add("map-destination");

    return {'map': map, 'start': [startLat, startLng], 'end': [endLat, endLng]};
}

function itineraire(start, end, link) {
    console.log("Fonction itineraire() appelée");
    const settings = document.querySelector('a[href="/account/profile/"] svg');
    const profile = document.querySelector('a#change-profile');
    console.log(settings, profile);
    const svg = settings.cloneNode(true);
    profile.appendChild(svg);
    try {
        if (!link) throw new Error("Conteneur des contrôles Leaflet introuvable.");
        link.href = `https://www.google.com/maps/dir/?api=1&origin=${start[0]},${start[1]}&destination=${end[0]},${end[1]}&travelmode=driving`;
    } catch (error) {
        console.error("Erreur lors de l'ajout du lien Google Maps:", error);
    }    
}