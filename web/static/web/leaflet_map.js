// Create a Leaflet map instance
var map = L.map('map', {attributionControl: false}).setView([48.621136, 18.337101], 14);

// Add a tile layer to the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(map);

// Add a marker to the map
//let marker = L.marker([48.621136, 18.337101]).addTo(map);