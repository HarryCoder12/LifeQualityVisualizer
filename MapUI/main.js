// Create the map
var map = new ol.Map({
    target: 'map', // The div where the map will be placed
    layers: [
        // Add a base layer
        new ol.layer.Tile({
            source: new ol.source.OSM() // OpenStreetMap
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([0, 0]), // Center the map (in lon/lat)
        zoom: 2 // Initial zoom level
    })
});

// Create a vector layer to hold GeoJSON data
var vectorLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
        // URL to your GeoJSON file
        url: 'path/to/your/file.geojson',
        format: new ol.format.GeoJSON()
    })
});

// Add the vector layer with GeoJSON to the map
map.addLayer(vectorLayer);